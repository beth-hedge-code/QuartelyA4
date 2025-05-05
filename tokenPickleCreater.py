# Authenticate the Gmail API using OAuth 2.0 
# and send a test email.
# This also generates a token.pickle file, 
# which saves the user’s access token so they 
# don’t have to re-authenticate each time.

from email.mime.text import MIMEText # Builds email content
import os, base64, pickle  # File handling, encoding, and saving credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # OAuth flow
from google.auth.transport.requests import Request # Token refresh
from googleapiclient.discovery import build # Builds Gmail service

SCOPES = ['https://www.googleapis.com/auth/gmail.send'] # Required Gmail scope to send emails

def get_gmail_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token) # loads saved creditials avoiding re-authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request()) #Try refreshing the token
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080) # Start new OAuth login in browser
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token) # Save new credentials for next time
    return build("gmail", "v1", credentials=creds)  # Returns an authorized Gmail API client

def send_email(subject, body, to):
    print("Sending email...")
    service = get_gmail_service() # Get authenticated service
    message = MIMEText(body, "html") # Email body is HTML-formatted
    message["to"] = to
    message["from"] = "me" # 'me' is the authenticated user
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()  # Encode the message for Gmail API
    message_body = {"raw": raw}
    sent = service.users().messages().send(userId="me", body=message_body).execute()
    print(f"✅ Email sent. Message ID: {sent['id']}") #confirmation message

if __name__ == "__main__":
    send_email(
        subject="✅ Gmail OAuth Test",
        body="<p>This is a test email sent via Gmail API and OAuth.</p>",
        to="your_email@gmail.com"  # replace with your real email
    )
