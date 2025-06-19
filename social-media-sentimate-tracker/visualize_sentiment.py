import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import os

# -------------------------------
# 1. Load Sentiment Data
# -------------------------------
input_path = "data/sentiment_tweets_20250613_2005.csv"  # Change to your latest sentiment file

if not os.path.exists(input_path):
    print(f"❌ File '{input_path}' not found. Run 'analyse_sentiment.py' first.")
    exit()

df = pd.read_csv(input_path)
df_cleaned = pd.read_csv(input_path)
# -------------------------------
# 2. Count Sentiment Labels
# -------------------------------
sentiment_counts = df['sentiment'].value_counts()

# -------------------------------
# 3. Plot Bar Chart
# -------------------------------
plt.figure(figsize=(8, 5))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="coolwarm")
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Tweets")
plt.tight_layout()
plt.savefig("data/sentiment_bar_chart.png")
plt.show()

# -------------------------------
# 4. Optional: Pie Chart
# -------------------------------
plt.figure(figsize=(6, 6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=sns.color_palette("coolwarm"))
plt.title("Sentiment Share")
plt.tight_layout()
plt.savefig("data/sentiment_pie_chart.png")
plt.show()

print("✅ Sentiment charts saved as PNG files in /data/")

# -------------------------------
# 5. Generate Word Cloud
# -------------------------------

all_text = ' '.join(str(t) for t in df_cleaned['cleaned_text'])

custom_stopwords = set(STOPWORDS)
custom_stopwords.update(['india', 'indian', 'today', 'news', 'amp'])  # add your own irrelevant words

wordcloud = WordCloud(
    width=1000,
    height=600,
    background_color='white',
    stopwords=custom_stopwords,
    collocations=False,
    colormap='viridis'
).generate(all_text)

plt.figure(figsize=(12, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of Tweets", fontsize=18)
plt.tight_layout()
plt.savefig("data/wordcloud.png")
plt.show()