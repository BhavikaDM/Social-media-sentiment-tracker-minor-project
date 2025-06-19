import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import os

# -------------------------------
# 1. Load Cleaned Tweet Data
# -------------------------------
input_path = "data/cleaned_tweets_20250613_2004.csv"  # Update this to your latest cleaned file

if not os.path.exists(input_path):
    print(f"❌ File '{input_path}' not found. Run 'clean_tweets.py' first.")
    exit()

df = pd.read_csv(input_path)

# -------------------------------
# 2. Initialize Sentiment Analyzer
# -------------------------------
analyzer = SentimentIntensityAnalyzer()

# -------------------------------
# 3. Sentiment Classification Function
# -------------------------------
def get_sentiment(text):
    score = analyzer.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return 'positive'
    elif compound <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# -------------------------------
# 4. Apply Sentiment Analysis
# -------------------------------
df['sentiment'] = df['cleaned_text'].apply(lambda x: get_sentiment(str(x)))

# -------------------------------
# 5. Save Result
# -------------------------------
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_path = f"data/sentiment_tweets_{timestamp}.csv"
df.to_csv(output_path, index=False)

print(f"✅ Sentiment analysis complete. Saved to: {output_path}")
