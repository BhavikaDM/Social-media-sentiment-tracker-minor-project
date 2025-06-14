import pandas as pd
import re
import emoji
import nltk
from nltk.tokenize import word_tokenize
from datetime import datetime
import os

# Optional: download NLTK tokenizer if not already downloaded
nltk.download('punkt')

# -------------------------------
# 1. Define the Cleaning Function
# -------------------------------
def clean_text(text, tokenize=False):
    text = re.sub(r"http\S+", "", text)                      # Remove URLs
    text = re.sub(r"@\w+", "", text)                         # Remove mentions
    text = emoji.replace_emoji(text, replace='')             # Remove emojis
    text = re.sub(r"[^\w\s]", "", text)                      # Remove special characters
    text = text.lower()                                      # Lowercase
    text = re.sub(r"\s+", " ", text).strip()                 # Trim extra whitespace
    if tokenize:
        return word_tokenize(text)
    else:
        return text

# -------------------------------
# 2. Load Raw Tweet Data
# -------------------------------
input_path = "data/tweets_20250613_2002.csv"  # Change this if your raw file name is different

if not os.path.exists(input_path):
    print(f"❌ File '{input_path}' not found. Make sure you fetched tweets first.")
    exit()

df_raw = pd.read_csv(input_path)

# -------------------------------
# 3. Apply Cleaning
# -------------------------------
df_raw["cleaned_text"] = df_raw["text"].apply(lambda x: clean_text(str(x), tokenize=False))

# -------------------------------
# 4. Save Cleaned Data
# -------------------------------
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_path = f"data/cleaned_tweets_{timestamp}.csv"
df_raw.to_csv(output_path, index=False)

print(f"✅ Cleaned tweets saved to: {output_path}")
