Friday project: Quarterly Assessment 4

Goal: create an AI-Powered News Newsletter Generator that automates the process of keeping users informed about the latest news.

You want a system that:
    1) fetches the latest news by retrieving articles on topics of interest from reliable sources. 
    2) summarizes the main points with an LLM to condense the lengthy article into a concise email-friendly summary, and 
    3) deliver the information via email to recipients. Since this email should be “automated,” you can do this by scheduling a script to
    run daily using a task scheduler (e.g., cron on macOS/Linux or Task Scheduler on Windows). It should run your python file.

🔐 Setup Instructions: API Keys & Authentication

To use this project, you’ll need to set up credentials for both OpenAI, NewsAPI, and Gmail OAuth 2.0 to authorize access and automate sending email summaries.

📌 1. Edit the .env File
    OPENAI_API_KEY=your_openai_api_key
    NEWS_API_KEY=your_newsapi_key
    EMAIL_RECIPIENTS=your_email@example.com,another@example.com
    Replace with your actual keys and recipient addresses.

🧠 2. Get Your OpenAI API Key
    Visit https://platform.openai.com/account/api-keys
    Log in and create a new key
    Paste it into the .env file as OPENAI_API_KEY

📰 3. Get Your NewsAPI Key
    Go to https://newsapi.org/register
    Sign up for a free account
    After registration, copy your API key
    Paste it into the .env file as NEWS_API_KEY

✉️ 4. Enable Gmail API & Get credentials.json
    Go to https://console.cloud.google.com/
    Create a new project (or reuse an existing one)
    Go to "APIs & Services" → "Library", search "Gmail API", and enable it
    Go to "APIs & Services" → "OAuth consent screen"
    Choose External, set up the form, and add yourself as a test user
    Go to "Credentials" → "Create Credentials" → "OAuth client ID"
    Choose Desktop App
    Download the credentials.json file
    Place credentials.json in the root project directory

🔑 5. Generate Your token.pickle (OAuth Token)
    Run the token setup script: tokenPickleCreater.py
    This will open a browser window for Google login. Once approved, it will create a token.pickle file that stores your secure access token.

You should be read to go now!!!