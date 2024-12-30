# src/utils/faq_api.py
import requests

class FAQAPI:
    def __init__(self):
        # Using API Ninjas FAQ API - sign up for free API key
        self.api_key = ""
        self.base_url = "https://api.api-ninjas.com/v1/facts"
    
    def get_fact(self):
        headers = {
            'X-Api-Key': self.api_key
        }
        try:
            response = requests.get(self.base_url, headers=headers)
            if response.status_code == 200:
                facts = response.json()
                return facts[0]['fact'] if facts else None
            return None
        except Exception as e:
            print(f"Error fetching fact: {e}")
            return None