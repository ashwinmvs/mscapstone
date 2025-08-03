"""
data_loader.py
Module for loading and preprocessing financial, macroeconomic, and sentiment data for the capstone project.
"""

import pandas as pd
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas_datareader.data as web

def load_price_data(symbols, start_date, end_date):
    """
    Load historical price and volume data for given symbols from Yahoo Finance or other sources.
    """
    # Placeholder: implement data loading logic
    return pd.DataFrame()

def load_macro_data():
    """
    Load real macroeconomic indicators (e.g., interest rates, inflation) from FRED.
    """
    start = '2020-01-01'
    end = '2025-07-31'
    # US 10-Year Treasury Constant Maturity Rate and CPI
    interest_rate = web.DataReader('DGS10', 'fred', start, end)
    inflation = web.DataReader('CPIAUCSL', 'fred', start, end)
    df = pd.concat([interest_rate, inflation], axis=1)
    df.columns = ['interest_rate', 'inflation']
    df = df.reset_index().rename(columns={'DATE': 'date'})
    return df

def load_sentiment_data(start_date='2025-07-01', end_date='2025-07-31'):
    """
    Load real sentiment data using news headlines and VADER sentiment analysis.
    Accepts start_date and end_date as YYYY-MM-DD strings.
    """
    NEWSAPI_KEY = 'f34c5143a525464eab65af295b328c6d'  # User's NewsAPI key
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "MELI"]
    analyzer = SentimentIntensityAnalyzer()
    all_data = []
    for symbol in symbols:
        url = f'https://newsapi.org/v2/everything?q={symbol}&from={start_date}&to={end_date}&sortBy=publishedAt&language=en&apiKey={NEWSAPI_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            for article in articles:
                headline = article['title']
                date = article['publishedAt'][:10]
                score = analyzer.polarity_scores(headline)['compound']
                all_data.append({'date': date, 'symbol': symbol, 'headline': headline, 'sentiment_score': score})
        else:
            print(f"NewsAPI error for {symbol}: {response.status_code} {response.text}")
    df = pd.DataFrame(all_data)
    return df
