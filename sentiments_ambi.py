from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import nltk
import time
from urllib.error import HTTPError
from config import COMPANY_TICKER

# Initialize VADER
nltk.download('vader_lexicon', quiet=True)
vader = SentimentIntensityAnalyzer()

def get_daily_sentiment():
    """Fetch and calculate daily sentiment scores for COMPANY_TICKER"""
    finviz_url = f'https://finviz.com/quote.ashx?t={COMPANY_TICKER}'
    
    try:
        # Fetch data with rate limiting
        req = Request(
            url=finviz_url,
            headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        )
        time.sleep(1)  # Respect rate limits
        html = BeautifulSoup(urlopen(req), features='html.parser')
        
        # Parse news table
        parsed_data = []
        for row in html.find(id='news-table').findAll('tr'):
                if row.a:
                    title = row.a.text
                    # Handle both date formats:
                    # "May-25-23 04:30PM" and "Today 04:30PM"
                    date_str = row.td.text.strip().split()[0]
                    
                    if date_str == 'Today':
                        date = pd.to_datetime('today').date()
                    else:
                        date = pd.to_datetime(date_str).date()
                    
                    parsed_data.append([date, title])
        
        # Calculate daily mean sentiment
        df = pd.DataFrame(parsed_data, columns=['date', 'title'])
        df['Sentiment'] = df['title'].apply(
            lambda x: vader.polarity_scores(x)['compound']
        )
        return df.groupby('date')['Sentiment'].mean().to_frame()
        
    except Exception as e:
        print(f"⚠️ Failed to get sentiment for {COMPANY_TICKER}: {str(e)}")
        return pd.DataFrame(columns=['Sentiment'])  # Return empty DataFrame
