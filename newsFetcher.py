#This file completes step 1 of this program
#Step 1: fetch the latest news by retrieving articles on topics of interest from reliable sources.

import os
import requests
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv("NEWS_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please set NEWS_API_KEY in your .env file.")

# Function to fetch news on a specific topic
def fetch_news(topic, language='en', page_size=5):
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': topic,
        'language': language,
        'pageSize': page_size,
        'apiKey': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        for i, article in enumerate(articles, 1):
            print(f"\nArticle {i}:")
            print(f"Title: {article['title']}")
            print(f"Source: {article['source']['name']}")
            print(f"URL: {article['url']}")
            print(f"Published At: {article['publishedAt']}")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Example usage
if __name__ == "__main__":
    topic = input("Enter a topic you're interested in: ")
    fetch_news(topic)