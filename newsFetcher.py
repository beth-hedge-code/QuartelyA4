#This file completes step 1 of this program
#Step 1: fetch the latest news by retrieving articles on topics of interest from reliable sources.

import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from environment variable
news_api_key = os.getenv("NEWS_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
print(f"OPENAI_API_KEY loaded: {openai_api_key is not None}")
print(f"NEWS_API_KEY loaded: {news_api_key is not None}")

client = OpenAI(api_key=openai_api_key)

# Step 1: Fetch articles
def fetch_articles(topic, max_results=3):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "pageSize": max_results,
        "sortBy": "relevancy",
        "language": "en",
        "apiKey": news_api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
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

# Step 3: Run pipeline
def summarize_news():
    topic = input("Enter a topic of interest: ").strip()
    articles = fetch_articles(topic)

    if not articles:
        print("No articles found or API error.")
        return

    for i, article in enumerate(articles, 1):
        print(f"\n📰 Article {i}: {article['title']}")
        print("🔗", article['url'])
        summary = summarize_article(article['title'], article.get('description'), article['url'])
        print("📄 Summary:")
        print(summary)
        print("-" * 60)

if __name__ == "__main__":
    summarize_news()