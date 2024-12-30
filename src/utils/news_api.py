# src/utils/news_api.py
import requests
from datetime import datetime

class NewsAPI:
    def __init__(self):
        # Using NewsAPI.org - sign up for free API key
        self.api_key = ""
        self.base_url = "https://newsapi.org/v2/top-headlines"
    
    def get_news(self, category="general", country="us", max_results=5):
        params = {
            "apiKey": self.api_key,
            "category": category,
            "country": country,
            "pageSize": max_results
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                news_data = response.json()
                return [{"title": article["title"], 
                        "description": article["description"],
                        "url": article["url"]} 
                        for article in news_data["articles"][:max_results]]
            return []
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []