# onferni
Onferni is a discord bot I designed for fun that is configured to be sarcastic and rude to general users, but polite to me. The key feature is that you can set individual personalities for each user and even specific responses using the same code template.
## Technologies Used

-   **Backend:** Python 3.8+
-   **Discord API Wrapper:** [discord.py](https://github.com/Rapptz/discord.py)
-   **LLM:** [Google Gemini API](https://ai.google.dev/)
-   **Environment Variables:** [python-dotenv](https://github.com/theskumar/python-dotenv)

## Setup and Installation

Follow these steps to get the bot running on your own machine or server.

### 1. Prerequisites

-   Python 3.8 or newer
-   A Discord account with a server you have "Manage Server" permissions on.
-   A Google account for the Gemini API key.

### 2. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```
### 3. Configure Your Keys

Create a file named .env in the project folder.

Add your secret keys to it like this:

```
DISCORD_BOT_TOKEN=your_discord_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```
### 5. Configure Personas

Edit persona.txt to set the bot's default personality.

Edit king_persona.txt and the user IDs in bot.py to customize special user rules.

### 6. Run the Bot

Launch the bot from your terminal.
```bash
python bot.py
```
