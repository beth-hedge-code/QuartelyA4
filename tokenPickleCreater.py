from email.mime.text import MIMEText
import os, base64, pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

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

def send_email(subject, body, to):
    print("Sending email...")
    service = get_gmail_service()
    message = MIMEText(body, "html")
    message["to"] = to
    message["from"] = "me"
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {"raw": raw}
    sent = service.users().messages().send(userId="me", body=message_body).execute()
    print(f"✅ Email sent. Message ID: {sent['id']}")

if __name__ == "__main__":
    send_email(
        subject="✅ Gmail OAuth Test",
        body="<p>This is a test email sent via Gmail API and OAuth.</p>",
        to="your_email@gmail.com"  # replace with your real email
    )
