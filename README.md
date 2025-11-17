# AI-Powered News Newsletter Generator

## Overview
Create an automated system that keeps users informed about the latest news by:

1. **Fetching the latest news** from reliable sources based on chosen topics.
2. **Summarizing the main points** using an LLM to produce concise, email-friendly summaries.
3. **Delivering automated email updates** using a scheduled script.

---

# Setup Instructions: API Keys & Authentication
To run this project, configure credentials for:
- **OpenAI API**
- **NewsAPI**
- **Gmail OAuth 2.0** (for automated email sending)

---

## 1. Create and Edit the `.env` File
Add:
```
OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_newsapi_key
EMAIL_RECIPIENTS=your_email@example.com,another@example.com
```
Replace with your actual keys and email addresses.

---

## 2. Get Your OpenAI API Key
1. Visit https://platform.openai.com/account/api-keys
2. Create a new key
3. Add it to `.env` under `OPENAI_API_KEY`

---

## 3. Get Your NewsAPI Key
1. Visit https://newsapi.org/register
2. Sign up and copy your key
3. Add it to `.env` as `NEWS_API_KEY`

---

## 4. Enable Gmail API & Download `credentials.json`
1. Visit https://console.cloud.google.com/
2. Create or use an existing project
3. Enable **Gmail API**
4. Configure **OAuth consent screen**
5. Create **OAuth Client ID → Desktop App**
6. Download `credentials.json`
7. Place it in the project root

---

## 5. Generate `token.pickle`
Run:
```
tokenPickleCreater.py
```
This will create a secure `token.pickle` after Google login.

---

# Automate Daily News Emails (Windows)
Use Windows Task Scheduler to run the script automatically.

## 1. Open Task Scheduler
- Press **Windows + S**
- Search **Task Scheduler**
- Select **Create Basic Task...**

---

## 2. Create the Daily Task
- **Name:** Send Daily News Email
- **Trigger:** Daily
- **Time:** e.g., 8:00 AM
- **Action:** Start a program

---

## 3. Configure Python and Script Path
**Program/script:**
```
C:\Users\YourName\AppData\Local\Programs\Python\PythonXXX\python.exe
```

**Add arguments:**
```
"C:\Users\YourName\Path\To\newsFetcher.py"
```

---

## 4. Finish and Test
- Click **Finish**
- Right-click the task → **Run**

You should receive the email within **30–60 seconds**.

