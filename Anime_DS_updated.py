import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
import re

# Importing data from CSV and examining its size
animes_import = pd.read_csv("animes_updated.csv")
animes = animes_import[['uid', 'title', 'synopsis', 'genre', 'aired', 'episodes', 'popularity', 'score']]
pd.set_option('display.max_columns', None)

# Getting the number of rows and columns
rows_cols = animes.shape
rows = rows_cols[0]
cols = rows_cols[1]

# Function to retrieve data using UID
def get_name_by_id(df, id_value):
    row = df[df['uid'] == id_value]
    if not row.empty:
        return row['title'].values[0]
    else:
        return None
    
def get_synopsis_by_id(df, id_value):
    row = df[df['uid'] == id_value]
    if not row.empty:
        return row['synopsis'].values[0]
    else:
        return None

# Checking for missing values
def find_empty_synopsis(df):
    return df[df['synopsis'].isnull()]['uid'].tolist()

empty_syn = find_empty_synopsis(animes)

def update_synopsis_by_id(df, id_value, new_synopsis):
    df.loc[df['uid'] == id_value, 'synopsis'] = new_synopsis

for uid in empty_syn:
    update_synopsis_by_id(animes, uid, "")

# Handling empty scores
animes = animes.copy()

def find_empty_score(df):
    return df[df['score'].isnull()]['uid'].tolist()

Null_scores_lst = find_empty_score(animes)
animes.dropna(subset=['score'], inplace=True)

# Handling all episodes that are empty
animes['episodes'] = animes['episodes'].fillna(-1)

# Creating column for years anime aired
isOneEpisode = animes['episodes'] == 1

def year_of_anime():
    years = []
    for i in range(len(animes)):
        aired = animes['aired'].iloc[i]
        if isOneEpisode.iloc[i] and aired != "Not available":
            if int(aired[-2:]) > 19:
                years.append(1900 + int(aired[-2:]))
            else:
                years.append(2000 + int(aired[-2:]))
        elif isOneEpisode.iloc[i] and aired == "Not available":
            years.append(0)
        elif aired[-1:] != "?":
            years.append(int(aired[-4:]))
        else:
            pattern = r'\b20\d{2}\b'
            matches = re.findall(pattern, aired)
            if matches:
                processed_matches = [int(match) for match in matches]
                years.append(processed_matches[0])
            else:
                years.append(0)  # Handle cases where no matches are found
    return years

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

animes['Years'] = animes['aired'].apply(years_from_aired)

# Using episodes to determine the size of anime
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

animes['Relative Length'] = animes['episodes'].apply(categorizeAnimes)

# Deleting duplicates
for col in animes.columns:
    if animes[col].apply(lambda x: isinstance(x, list)).any():
        animes[col] = animes[col].apply(tuple)

animes = animes.drop_duplicates()


# Converting columns to lists of strings
def convert_to_strLst(string):
    if pd.isna(string):
        return []
    return string.split()

# Ensure the relevant columns are lists of strings
animes['title'] = animes['title'].apply(convert_to_strLst)
animes['synopsis'] = animes['synopsis'].apply(convert_to_strLst)
animes['genre'] = animes['genre'].apply(lambda x: x.split(','))
animes['Relative Length'] = animes['Relative Length'].apply(convert_to_strLst)
animes['Years'] = animes['Years'].apply(lambda x: x if isinstance(x, list) else [str(x)])

### Clean genre column with clean_genre ###
def clean_genre(genre_string):
    if isinstance(genre_string, str):
        # Remove brackets, quotes, and unnecessary characters
        cleaned_string = re.sub(r"[\[\]']", "", genre_string)
        return [g.strip() for g in cleaned_string.split(",") if g.strip()]
    elif isinstance(genre_string, list):
        # If it's already a list, return it as is
        return genre_string
    else:
        return []

animes['genre'] = animes['genre'].apply(clean_genre)

# Combine the lists from each column into a new column called 'tags'
animes['tags'] = animes.apply(lambda row: row['title'] + row['synopsis'] + row['genre'] + row['Relative Length'] + row['Years'], axis=1)

# Drop duplicates based on specific columns (for example 'uid' and 'title')
animes = animes.drop_duplicates(subset=['uid', 'title'])
# Save to CSV
animes.to_csv('AnimesCleaned.csv', index=False)

