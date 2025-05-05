#Goal: Automate a daily process to:
#   Fetch top news articles
#   Summarize them with OpenAI
#   Format them into a clean HTML email
#   Send that email using Gmail


import os # Handles environment variables
import base64 # Encodes email in base64 for Gmail API
import pickle # Saves and loads Gmail API tokens
import requests # Makes HTTP requests to News API
from email.mime.text import MIMEText # Creates email format
from dotenv import load_dotenv # Loads .env file with secrets
from openai import OpenAI # Connects to OpenAI for summarizing
from google_auth_oauthlib.flow import InstalledAppFlow # Auth for Gmail API
from google.auth.transport.requests import Request
from googleapiclient.discovery import build  # Builds Gmail API client


# SETUP & API KEYS
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
load_dotenv()  # Load variables like API keys from .env file

# Get the API key from environment variable
news_api_key = os.getenv("NEWS_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
email_recipients = os.getenv("EMAIL_RECIPIENTS").split(',')  # Split recipients if multiple

client = OpenAI(api_key=openai_api_key)  # Authenticate OpenAI client

# Step 1: Fetch articles
#Purpose: Gets the Top headlines from NewsApi
def fetch_top_articles(max_results=3):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "language": "en",
        "pageSize": max_results,
        "apiKey": news_api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("NewsAPI error:", response.text)
        return []
    return response.json().get("articles", [])

# Step 2: Summarize with OpenAI
# Purpose: Sends the article content to OpenAI and 
# receives a short, clean summary in bullet points.
def summarize_article(title, description, url):
    prompt = (
        f"Summarize the following news story in 2-3 email-friendly bullet points:\n\n"
        f"Title: {title}\n\n"
        f"Description: {description or 'No description available.'}\n\n"
        f"Link: {url}\n\n"
        f"Keep it professional and concise."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Step 3: Compose HTML body
# Purpose: Converts the summaries into styled HTML format 
# with headings and line breaks for each article.
def build_email_body(summaries):
    html = "<h2>📰 Your Daily News Digest</h2>"
    for i, summary in enumerate(summaries, 1):
        html += f"<h3>Article {i}</h3><p>{summary.replace(chr(10), '<br>')}</p><hr>"
    return html

# Step 4: Gmail API auth and service
# Purpose: Handles Gmail OAuth authentication. 
# Saves credentials to avoid repeating login.
def get_gmail_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("gmail", "v1", credentials=creds)

# Step 5: Send email
# Purpose: Builds the message, encodes it for Gmail API, 
# and sends it to the recipient(s).
def send_email(subject, html_body, recipients):
    service = get_gmail_service()
    message = MIMEText(html_body, "html")
    message["to"] = ", ".join(recipients)
    message["from"] = "me"
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {"raw": raw}

    sent = service.users().messages().send(userId="me", body=message_body).execute()
    print(f"✅ Email sent! Message ID: {sent['id']}")

# Run the entire pipeline
def main():
    articles = fetch_top_articles()
    if not articles:
        print("No news articles found.")
        return

    summaries = []
    for article in articles:
        summary = summarize_article(article["title"], article.get("description"), article["url"])
        summaries.append(summary)

    html = build_email_body(summaries)
    send_email("🗞️ Your Daily News Digest", html, email_recipients)

#Runs the Program
if __name__ == "__main__":
    main()