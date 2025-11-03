"""
Enhanced Feature Engineering for Gold Price Prediction
This module adds additional features that correlate with gold prices:
1. Oil prices (WTI/Brent crude)
2. Swiss Franc (CHF/USD)
3. News sentiment analysis
4. Additional currency indices (DXY - Dollar Index)
5. Treasury yields
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ===========================
# 1. OIL PRICE DATA
# ===========================
def fetch_oil_data(start_date='2009-01-01', end_date=None):
    """
    Fetch crude oil prices using yfinance.
    WTI Crude Oil ticker: CL=F
    Brent Crude Oil ticker: BZ=F
    
    Parameters:
    -----------
    start_date: str, start date for data
    end_date: str, end date for data (defaults to today)
    
    Returns:
    --------
    pd.DataFrame with oil prices
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print("Fetching WTI Crude Oil data...")
    oil_wti = yf.download('CL=F', start=start_date, end=end_date, progress=False)
    
    # Rename columns to clarify it's oil data
    oil_df = pd.DataFrame()
    oil_df['Date'] = oil_wti.index
    oil_df['Oil_Open'] = oil_wti['Open'].values
    oil_df['Oil_High'] = oil_wti['High'].values
    oil_df['Oil_Low'] = oil_wti['Low'].values
    oil_df['Oil_Close'] = oil_wti['Close'].values
    oil_df['Oil_Volume'] = oil_wti['Volume'].values
    
    oil_df['Date'] = pd.to_datetime(oil_df['Date']).dt.tz_localize(None)
    oil_df = oil_df.reset_index(drop=True)
    
    print(f"✅ Oil data fetched: {len(oil_df)} rows")
    return oil_df


# ===========================
# 2. SWISS FRANC DATA
# ===========================
def fetch_chf_data(start_date='2009-01-01', end_date=None):
    """
    Fetch Swiss Franc to USD exchange rate.
    Ticker: CHF=X
    
    Parameters:
    -----------
    start_date: str, start date for data
    end_date: str, end date for data
    
    Returns:
    --------
    pd.DataFrame with CHF/USD rates
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print("Fetching Swiss Franc (CHF/USD) data...")
    chf = yf.download('CHF=X', start=start_date, end=end_date, progress=False)
    
    chf_df = pd.DataFrame()
    chf_df['Date'] = chf.index
    chf_df['CHF_Open'] = chf['Open'].values
    chf_df['CHF_High'] = chf['High'].values
    chf_df['CHF_Low'] = chf['Low'].values
    chf_df['CHF_Close'] = chf['Close'].values
    
    chf_df['Date'] = pd.to_datetime(chf_df['Date']).dt.tz_localize(None)
    chf_df = chf_df.reset_index(drop=True)
    
    print(f"✅ CHF data fetched: {len(chf_df)} rows")
    return chf_df


# ===========================
# 3. DOLLAR INDEX (DXY)
# ===========================
def fetch_dxy_data(start_date='2009-01-01', end_date=None):
    """
    Fetch US Dollar Index (DXY).
    Ticker: DX-Y.NYB
    
    The Dollar Index measures USD strength against a basket of currencies.
    Gold typically has inverse correlation with DXY.
    
    Parameters:
    -----------
    start_date: str, start date for data
    end_date: str, end date for data
    
    Returns:
    --------
    pd.DataFrame with DXY values
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print("Fetching US Dollar Index (DXY) data...")
    dxy = yf.download('DX-Y.NYB', start=start_date, end=end_date, progress=False)
    
    dxy_df = pd.DataFrame()
    dxy_df['Date'] = dxy.index
    dxy_df['DXY_Open'] = dxy['Open'].values
    dxy_df['DXY_High'] = dxy['High'].values
    dxy_df['DXY_Low'] = dxy['Low'].values
    dxy_df['DXY_Close'] = dxy['Close'].values
    
    dxy_df['Date'] = pd.to_datetime(dxy_df['Date']).dt.tz_localize(None)
    dxy_df = dxy_df.reset_index(drop=True)
    
    print(f"✅ DXY data fetched: {len(dxy_df)} rows")
    return dxy_df


# ===========================
# 4. TREASURY YIELDS (10-Year)
# ===========================
def fetch_treasury_data(start_date='2009-01-01', end_date=None):
    """
    Fetch 10-Year Treasury Yield.
    Ticker: ^TNX
    
    Treasury yields affect gold as they represent risk-free return.
    Higher yields can reduce gold's appeal.
    
    Parameters:
    -----------
    start_date: str, start date for data
    end_date: str, end date for data
    
    Returns:
    --------
    pd.DataFrame with treasury yields
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print("Fetching 10-Year Treasury Yield data...")
    tnx = yf.download('^TNX', start=start_date, end=end_date, progress=False)
    
    tnx_df = pd.DataFrame()
    tnx_df['Date'] = tnx.index
    tnx_df['TNX_Open'] = tnx['Open'].values
    tnx_df['TNX_High'] = tnx['High'].values
    tnx_df['TNX_Low'] = tnx['Low'].values
    tnx_df['TNX_Close'] = tnx['Close'].values
    
    tnx_df['Date'] = pd.to_datetime(tnx_df['Date']).dt.tz_localize(None)
    tnx_df = tnx_df.reset_index(drop=True)
    
    print(f"✅ Treasury Yield data fetched: {len(tnx_df)} rows")
    return tnx_df


# ===========================
# 5. NEWS SENTIMENT ANALYSIS
# ===========================
def fetch_news_sentiment(api_key=None, keywords=['gold', 'precious metals'], start_date='2009-01-01'):
    """
    Fetch news sentiment using NewsAPI or alternative sources.
    
    NOTE: This requires an API key from newsapi.org (free tier available)
    Free tier: 100 requests/day, 1 month historical data
    
    For production, consider:
    - NewsAPI (newsapi.org) - Free tier available
    - Alpha Vantage News Sentiment API
    - GDELT Project (free but complex)
    - Twitter/X API for real-time sentiment
    
    Parameters:
    -----------
    api_key: str, NewsAPI key
    keywords: list, keywords to search for
    start_date: str, start date
    
    Returns:
    --------
    pd.DataFrame with sentiment scores by date
    """
    if api_key is None:
        print("⚠️  No NewsAPI key provided. Sentiment feature will be skipped.")
        print("📝 To enable news sentiment:")
        print("   1. Sign up at https://newsapi.org (free tier: 100 requests/day)")
        print("   2. Get your API key")
        print("   3. Pass it to this function: fetch_news_sentiment(api_key='your_key')")
        return None
    
    try:
        from newsapi import NewsApiClient
        newsapi = NewsApiClient(api_key=api_key)
        
        # NewsAPI free tier only allows 1 month back, so we'll create a mock for historical
        print("⚠️  NewsAPI free tier has limitations. Creating sample sentiment data...")
        
        # For demonstration, create a placeholder with neutral sentiment
        # In production, you'd need to:
        # 1. Use paid API for historical data
        # 2. Web scrape historical news
        # 3. Use pre-built sentiment datasets
        
        dates = pd.date_range(start=start_date, end=datetime.now(), freq='D')
        sentiment_df = pd.DataFrame({
            'Date': dates,
            'News_Sentiment': 0.0,  # Neutral sentiment placeholder
            'News_Count': 0
        })
        
        print(f"📰 News sentiment placeholder created: {len(sentiment_df)} rows")
        print("💡 Replace this with actual API calls or historical sentiment data")
        return sentiment_df
        
    except ImportError:
        print("⚠️  newsapi-python not installed. Run: pip install newsapi-python")
        return None


# ===========================
# 6. ALTERNATIVE: VADER SENTIMENT ON HEADLINES
# ===========================
def analyze_headlines_vader(headlines_df):
    """
    Analyze sentiment of headlines using VADER (no API key needed).
    
    Parameters:
    -----------
    headlines_df: DataFrame with 'Date' and 'Headline' columns
    
    Returns:
    --------
    DataFrame with sentiment scores
    """
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        
        def get_sentiment(text):
            if pd.isna(text):
                return 0.0
            scores = analyzer.polarity_scores(text)
            return scores['compound']  # -1 (negative) to +1 (positive)
        
        headlines_df['Sentiment'] = headlines_df['Headline'].apply(get_sentiment)
        
        # Aggregate by date
        daily_sentiment = headlines_df.groupby('Date').agg({
            'Sentiment': 'mean',
            'Headline': 'count'
        }).reset_index()
        daily_sentiment.columns = ['Date', 'News_Sentiment', 'News_Count']
        
        return daily_sentiment
        
    except ImportError:
        print("⚠️  vaderSentiment not installed. Run: pip install vaderSentiment")
        return None


# ===========================
# 7. MERGE ALL FEATURES
# ===========================
def merge_all_features(base_df, oil_df=None, chf_df=None, dxy_df=None, 
                       tnx_df=None, sentiment_df=None):
    """
    Merge all additional features with the base dataframe.
    
    Parameters:
    -----------
    base_df: DataFrame with gold/silver data
    oil_df: DataFrame with oil prices
    chf_df: DataFrame with CHF/USD rates
    dxy_df: DataFrame with Dollar Index
    tnx_df: DataFrame with Treasury yields
    sentiment_df: DataFrame with news sentiment
    
    Returns:
    --------
    Merged DataFrame with all features
    """
    result = base_df.copy()
    
    if oil_df is not None:
        print("Merging oil data...")
        result = pd.merge(result, oil_df, on='Date', how='left')
    
    if chf_df is not None:
        print("Merging CHF data...")
        result = pd.merge(result, chf_df, on='Date', how='left')
    
    if dxy_df is not None:
        print("Merging DXY data...")
        result = pd.merge(result, dxy_df, on='Date', how='left')
    
    if tnx_df is not None:
        print("Merging Treasury Yield data...")
        result = pd.merge(result, tnx_df, on='Date', how='left')
    
    if sentiment_df is not None:
        print("Merging sentiment data...")
        result = pd.merge(result, sentiment_df, on='Date', how='left')
    
    # Forward fill missing values (for non-trading days)
    result = result.fillna(method='ffill')
    
    print(f"\n✅ All features merged! Final shape: {result.shape}")
    print(f"Columns: {result.columns.tolist()}")
    
    return result


# ===========================
# 8. CALCULATE DERIVED FEATURES
# ===========================
def add_derived_features(df):
    """
    Add derived features like ratios and correlations.
    
    Parameters:
    -----------
    df: DataFrame with all raw features
    
    Returns:
    --------
    DataFrame with additional derived features
    """
    print("\nCalculating derived features...")
    
    # Gold/Oil ratio (often tracked by traders)
    if 'Oil_Close' in df.columns:
        df['Gold_Oil_Ratio'] = df['Gold_Close'] / df['Oil_Close']
        print("✅ Gold/Oil Ratio added")
    
    # DXY inverse correlation indicator
    if 'DXY_Close' in df.columns:
        df['Gold_DXY_Inverse'] = -df['DXY_Close']  # Negative for inverse relationship
        print("✅ Gold/DXY Inverse added")
    
    # Treasury yield spread impact
    if 'TNX_Close' in df.columns:
        df['Gold_Yield_Spread'] = df['Gold_Close'] / (df['TNX_Close'] + 1)  # +1 to avoid div by zero
        print("✅ Gold/Yield Spread added")
    
    # Volatility features
    if 'Oil_High' in df.columns and 'Oil_Low' in df.columns:
        df['Oil_Volatility'] = df['Oil_High'] - df['Oil_Low']
        print("✅ Oil Volatility added")
    
    if 'CHF_High' in df.columns and 'CHF_Low' in df.columns:
        df['CHF_Volatility'] = df['CHF_High'] - df['CHF_Low']
        print("✅ CHF Volatility added")
    
    return df


# ===========================
# 9. MAIN INTEGRATION FUNCTION
# ===========================
def integrate_all_features(base_df, start_date='2009-01-01', newsapi_key=None):
    """
    Main function to fetch and integrate all additional features.
    
    Parameters:
    -----------
    base_df: DataFrame with existing gold/silver data
    start_date: str, start date for fetching data
    newsapi_key: str, optional NewsAPI key for sentiment
    
    Returns:
    --------
    Enhanced DataFrame with all features
    """
    print("=" * 60)
    print("FETCHING ADDITIONAL FEATURES FOR GOLD PRICE PREDICTION")
    print("=" * 60)
    
    # Fetch all data sources
    oil_df = fetch_oil_data(start_date)
    chf_df = fetch_chf_data(start_date)
    dxy_df = fetch_dxy_data(start_date)
    tnx_df = fetch_treasury_data(start_date)
    
    # Sentiment (optional, requires API key)
    sentiment_df = None
    if newsapi_key:
        sentiment_df = fetch_news_sentiment(newsapi_key, start_date=start_date)
    
    # Merge all features
    enhanced_df = merge_all_features(
        base_df, 
        oil_df=oil_df,
        chf_df=chf_df,
        dxy_df=dxy_df,
        tnx_df=tnx_df,
        sentiment_df=sentiment_df
    )
    
    # Add derived features
    enhanced_df = add_derived_features(enhanced_df)
    
    print("\n" + "=" * 60)
    print("✅ FEATURE INTEGRATION COMPLETE!")
    print("=" * 60)
    
    return enhanced_df


if __name__ == "__main__":
    print("Enhanced features module loaded.")
    print("Import this module in your notebook to use these functions.")
