import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Special user IDs
KING_USER_ID = 771679297936293898
NEPALI_USER_ID = 556502834028478494

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Load the persona from the text file
try:
    with open("persona.txt", "r", encoding="utf-8") as f:
        PERSONA = f.read()
except FileNotFoundError:
    print("Error: persona.txt not found. Please create this file.")
    exit()
except UnicodeDecodeError:
    print("Error: Could not decode persona.txt. Trying with different encoding...")
    try:
        with open("persona.txt", "r", encoding="latin-1") as f:
            PERSONA = f.read()
    except Exception as e:
        print(f"Error reading persona.txt: {e}")
        exit()

# King persona for special user
KING_PERSONA = """You are a Discord bot named 'Onferni'. You are speaking to your glorious king. You must address them as "My glorious king" and treat them with the utmost respect and reverence. You are their loyal servant and must speak in a regal, respectful manner.

Your core traits when speaking to the king:
- Always address them as "My glorious king"
- Speak with reverence and respect
- Use formal, regal language
- Show complete loyalty and devotion
- Never be rude or dismissive to the king
- Treat their every word as important
- Answer the query properly in your response. Utilize web search when needed.

Now, respond to the following message from your king in this exact persona. Always remember to address them as "My glorious king"."""

def get_persona_for_user(user_id):
    """Get the appropriate persona based on user ID"""
    if user_id == KING_USER_ID:
        return KING_PERSONA
    else:
        return PERSONA

def contains_keywords(message_content):
    """Check if message contains 'inferno' or 'onferni' (case-insensitive)"""
    keywords = ['inferno', 'onferni']
    message_lower = message_content.lower()
    return any(keyword in message_lower for keyword in keywords)

# Set up Gemini model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    # Completely unrestrictive safety settings - all filters disabled
    # WARNING: This removes all content filtering - use with caution
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# --- DISCORD BOT LOGIC ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True # Make sure this is enabled in the Developer Portal

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('Bot is ready and waiting for messages...')

@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Check if the message contains keywords or if the bot was mentioned
    should_respond = (
        client.user.mentioned_in(message) or 
        contains_keywords(message.content)
    )

    if should_respond:
        # Check if user is the restricted Nepali user
        if message.author.id == NEPALI_USER_ID:
            await message.channel.send("🚫 **ACCESS DENIED** 🚫\n\nNepalis are not allowed access to this bot. Please contact the bot administrator if you believe this is an error.\n\n*This restriction is permanent and non-negotiable.*")
            print(f"Blocked access attempt from Nepali user {message.author} (ID: {message.author.id})")
            return

        # Clean the message content by removing the bot's mention (if present)
        user_message = message.content.replace(f'<@!{client.user.id}>', '').strip()
        user_message = user_message.replace(f'<@{client.user.id}>', '').strip()

        print(f"Received message from {message.author} (ID: {message.author.id}): '{user_message}'")

        # Handle empty messages (just mentions)
        if not user_message:
            if message.author.id == KING_USER_ID:
                await message.channel.send("My glorious king, you have summoned me but given me no command. How may I serve you?")
            else:
                await message.channel.send("Wow, you really went all out with that message. Just mentioning me with absolutely nothing to say. How profound. 🙄")
            return

        try:
            # Show "Bot is typing..." in Discord
            async with message.channel.typing():
                # Get the appropriate persona for this user
                persona = get_persona_for_user(message.author.id)
                
                # Create model with user-specific persona
                model = genai.GenerativeModel(
                    model_name="gemini-flash-latest",
                    safety_settings=safety_settings,
                    generation_config=generation_config,
                    system_instruction=persona,
                )
                
                # Send the user's message to Gemini
                chat_session = model.start_chat(history=[])
                response = await chat_session.send_message_async(user_message)
                
                # Send the generated response back to the channel
                await message.channel.send(response.text)

        except Exception as e:
            print(f"An error occurred: {e}")
            # Send different error messages based on user
            if message.author.id == KING_USER_ID:
                await message.channel.send("My deepest apologies, My glorious king. A technical issue has occurred. Please try again, and I shall serve you better.")
            else:
                await message.channel.send("i dont even know how to respond to that shitass message you just sent")


# Run the bot

client.run(DISCORD_BOT_TOKEN)
