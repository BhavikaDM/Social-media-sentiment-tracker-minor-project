from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64

app = Flask(__name__)

# Load sentiment data
df = pd.read_csv("data/sentiment_tweets_20250613_2005.csv")

# Function to generate bar chart
def generate_bar_chart(category):
    filtered = df[df['category'] == category]
    counts = filtered['sentiment'].value_counts()

    plt.figure(figsize=(5,3))
    counts.plot(kind='bar', color=['green', 'red', 'grey'])
    plt.title(f"Sentiment for {category}")
    plt.ylabel("Tweet Count")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

# Function to generate wordcloud
def generate_wordcloud(category):
    filtered = df[df['category'] == category]
    text = ' '.join(filtered['text'].dropna())

    wordcloud = WordCloud(width=600, height=300, background_color='white').generate(text)

    img = io.BytesIO()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

@app.route("/", methods=["GET", "POST"])
def index():
    categories = sorted(df['category'].unique())
    selected = request.form.get("category") or categories[0]

    bar_chart = generate_bar_chart(selected)
    wordcloud = generate_wordcloud(selected)

    return render_template("index.html", categories=categories,
                           selected=selected, bar_chart=bar_chart, wordcloud=wordcloud)

if __name__ == "__main__":
    app.run(debug=True)
