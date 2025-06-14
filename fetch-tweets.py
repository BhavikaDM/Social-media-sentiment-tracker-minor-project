import tweepy
import pandas as pd
import datetime

# Replace this with your real Bearer Token
BEARER_TOKEN = 'Replace_with_your_bearer_token'

# Initialize Tweepy Client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Define query for all categories (OR logic)
query = '( health OR hospital OR vaccine OR doctor OR fashion OR makeup OR style OR clothes OR politics OR election OR government)  lang:en -is:retweet'

#add this with paid api
#'''crime OR murder OR kidnap OR life OR gun OR police OR kill OR death OR accident OR rape OR abuse OR tsunami OR earthquake OR flood OR landslide OR rain OR forestfire OR forest OR global warming OR thunder strike OR life OR fire OR diet OR metgala OR nation OR safety OR BRICS OR IMF OR sport OR IPL OR criket OR BCCI OR ICC OR winner OR worldcup OR batsmen OR bowler OR'''

# Keywords by category
category_keywords = {
    'Health': ['health', 'hospital', 'doctor', 'vaccine', 'medicine', 'wellness','diet'],
    'Fashion': ['fashion', 'style', 'makeup', 'outfit', 'clothes', 'runway','metgala'],
    'Politics': ['politics', 'government', 'election', 'policy', 'president', 'minister','nation','safety','national affairs','BRICS','IMF'],
    #'Sports': ['sport','IPL', 'cricket','BCCI','ICC','winner','worldcup','batsmen','bowler'],
    #'Natural Disaster': ['tsunami','earthquake','flood','landslide','rain','forestfire','forest','global warming','thunder strike','life','fire'],
    #'Crime':['crime','murder','kidnap','life','gun','police','shoot','kill','death','accident','rape','abuse']
}

# Function to assign category
def get_category(text):
    text = text.lower()
    for category, keywords in category_keywords.items():
        if any(keyword in text for keyword in keywords):
            return category
    return 'Other'

# Fetch tweets
response = client.search_recent_tweets(query=query,
                                       tweet_fields=['created_at', 'text', 'author_id'],
                                       max_results=40)

# Parse and categorize tweets
tweets_data = []
for tweet in response.data:
    category = get_category(tweet.text)
    tweets_data.append({
        'created_at': tweet.created_at,
        'author_id': tweet.author_id,
        'text': tweet.text,
        'category': category
    })

# Save to CSV
df = pd.DataFrame(tweets_data)
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
df.to_csv(f"data/tweets_{timestamp}.csv", index=False)

print(f"✅ {len(df)} tweets saved with categories to data/tweets_{timestamp}.csv")
