#This file completes step 1 of this program
#Step 1: fetch the latest news by retrieving articles on topics of interest from reliable sources.

import os
import base64
import pickle
import requests
from email.mime.text import MIMEText
from dotenv import load_dotenv
from openai import OpenAI
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# Load the environment variables from the .env file
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
load_dotenv()

# Debug check
print("EMAIL_RECIPIENTS =", os.getenv("EMAIL_RECIPIENTS"))

email_recipients = os.getenv("EMAIL_RECIPIENTS").split(',')

# Get the API key from environment variable
news_api_key = os.getenv("NEWS_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
email_recipients = os.getenv("EMAIL_RECIPIENTS").split(',')

client = OpenAI(api_key=openai_api_key)

# Step 1: Fetch articles
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
def build_email_body(summaries):
    html = "<h2>📰 Your Daily News Digest</h2>"
    for i, summary in enumerate(summaries, 1):
        html += f"<h3>Article {i}</h3><p>{summary.replace(chr(10), '<br>')}</p><hr>"
    return html

# Step 4: Gmail API auth and service
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

if __name__ == "__main__":
    main()