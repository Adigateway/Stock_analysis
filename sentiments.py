import requests
from transformers import pipeline
from datetime import datetime

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline(
            "text-classification", 
            model="finiteautomata/bertweet-base-sentiment-analysis"
        )
    
    def get_news(self, ticker, date):
        """Get news headlines for a given date (mock implementation)"""
        date_str = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        return [
            "Apple announces breakthrough in AI chip technology",
            "Market reacts positively to Apple's earnings report"
        ]
    
    def analyze_day(self, ticker, date):
        headlines = self.get_news(ticker, date)
        sentiments = [self.analyzer(h) for h in headlines]
        pos_score = sum(1 for s in sentiments if s['label'] == 'POSITIVE')
        return pos_score / len(headings) if headlines else 0.5