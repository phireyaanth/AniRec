import pandas as pd
import ast
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Load necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Option 1: Basic safe reading with escape character
df = pd.read_csv("animes_updated.csv")


# Drop unnecessary columns
df.drop(columns=["img_url", "link"], inplace=True)

# Drop rows with any missing values
df.dropna(inplace=True)

# Function to clean text (fix encoding issues, remove punctuation, lowercase, remove URLs)
def clean_text(text):
    if pd.isna(text):  # Handle missing values
        return ""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub('<.*?>+', '', text)  # Remove HTML tags
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove punctuation
    return text.strip()

# Extract years from aired column
def years_from_aired(aired):
    patterns = [
        r'\b\d{4}\b',
        r'\d{1,2}-\w{3}-\d{2,4}',
    ]
    
    if "Not available" in aired or aired.strip() == "?":
        return []
    
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, aired)
        for match in matches:
            if pattern == r'\b\d{4}\b':
                years.append(match)
            elif pattern == r'\d{1,2}-\w{3}-\d{2,4}':
                date_parts = match.split('-')
                year = date_parts[-1]
                if len(year) == 2:
                    year = "19" + year if int(year) > 19 else "20" + year
                years.append(year)
    
    return years

df['Years'] = df['aired'].apply(years_from_aired)

# Apply text preprocessing steps
df["title"] = df["title"].apply(clean_text)
df["synopsis"] = df["synopsis"].apply(clean_text)

# Convert genre from string to list (if stored as a string)
def convert_genre(genre_string):
    if isinstance(genre_string, str) and genre_string.startswith("["):
        return ast.literal_eval(genre_string)  # Convert string to list
    return genre_string  # Return as-is if it's already a list

df["genre"] = df["genre"].apply(convert_genre)

# Function to categorize anime based on episode count
def categorizeAnimes(episodes):
    if episodes == -1:
        return "Length Unavailable"
    elif episodes == 1:
        return "OVA"
    elif episodes < 7:
        return "Mini"
    elif episodes < 14:
        return "Small"
    elif episodes < 27:
        return "Average"
    elif episodes < 100:
        return "Large"
    else:
        return "Xtra Large"

df['Relative Length'] = df['episodes'].apply(categorizeAnimes)

# Remove leading/trailing spaces in column names
df.columns = df.columns.str.strip()

# Remove duplicate rows based on UID
df.drop_duplicates(subset=["uid"], inplace=True)

# Save the cleaned dataset
df.to_csv("AnimesCleaned.csv", index=False)

print("✅ Data cleaning complete! Saved as 'AnimesCleaned.csv'")
