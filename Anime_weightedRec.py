import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import ast

# Load both DataFrames
animes = pd.read_csv('AnimesCleaned.csv')  # For TF-IDF and cosine similarity
animes_updated = pd.read_csv('animes_updated.csv')  # For titles and UIDs

# Example custom weights for different features
title_weight = 0.3
synopsis_weight = 2.0
genre_weight = 2.7
relative_length_weight = 1.7
years_weight = 1.0

# Convert 'genre' from string to list of strings in the cleaned DataFrame
animes['genre'] = animes['genre'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Ensure proper data type and content for the other columns
animes['title'] = animes['title'].apply(lambda x: x.split() if isinstance(x, str) else x)
animes['synopsis'] = animes['synopsis'].apply(lambda x: x.split() if isinstance(x, str) else x)
animes['Relative Length'] = animes['Relative Length'].apply(lambda x: [x] if isinstance(x, str) else x)
animes['Years'] = animes['Years'].apply(lambda x: [str(x)] if not isinstance(x, list) else x)

# Create the 'tags' column with custom weights
def apply_feature_weights(row, title_weight, synopsis_weight, genre_weight, relative_length_weight, years_weight):
    title = row['title'] * int(title_weight) if isinstance(row['title'], list) else []
    synopsis = row['synopsis'] * int(synopsis_weight) if isinstance(row['synopsis'], list) else []
    genre = row['genre'] * int(genre_weight) if isinstance(row['genre'], list) else []
    
    if row['Relative Length'] == 'OVA':
        relative_length = row['Relative Length'] * 0.1  # Low weight for OVA
    else:
        relative_length = row['Relative Length'] * int(relative_length_weight) if isinstance(row['Relative Length'], list) else []
    
    years = row['Years'] * int(years_weight) if isinstance(row['Years'], list) else []
    
    # Combine all features into a single 'tags' column
    return title + synopsis + genre + relative_length + years

# Apply the function to create the 'tags' column
animes['tags'] = animes.apply(lambda row: apply_feature_weights(
    row, title_weight, synopsis_weight, genre_weight, relative_length_weight, years_weight), axis=1)

# Clean the 'tags' column to remove extra commas, quotes, etc.
animes['tags'] = animes['tags'].apply(lambda x: ' '.join(x))

# Perform TF-IDF vectorization on the cleaned 'tags' column
try:
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(animes['tags'])
except ValueError as e:
    print(f"Error during TF-IDF: {e}")
    print("Trying TF-IDF without stop words...")
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(animes['tags'])

# Compute cosine similarity using the TF-IDF matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Save the TF-IDF matrix and cosine similarity matrix for reuse in Flask app
with open('tfidf_matrix.pkl', 'wb') as f:
    pickle.dump(tfidf_matrix, f)
np.save('cosine_sim.npy', cosine_sim)

# Recommendation function 
def recommend_anime(uid, df, cosine_sim):
    try:
        idx = df.index[df['uid'] == uid].tolist()[0]
    except IndexError:
        return f"No anime found with UID {uid}"

    # Get similarity scores and sort
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 recommendations, excluding the input anime

    # Get the indices of the recommended animes
    anime_indices = [i[0] for i in sim_scores]

    # Retrieve the recommended animes
    recommended_animes = animes_updated.loc[animes_updated['uid'].isin(df.iloc[anime_indices]['uid'])]

    # Filter out animes that have the tag "Hentai"
    recommended_animes = recommended_animes[~recommended_animes['genre'].apply(lambda x: 'Hentai' in x)]

    # Print out the UID and title of the recommended animes
    if not recommended_animes.empty:
        print("Recommended Animes (excluding Hentai):")
        for idx, row in recommended_animes.iterrows():
            print(f"UID: {row['uid']}, Title: {row['title']}")
    else:
        print("No recommendations available (all recommended animes had the 'Hentai' tag).")

    return recommended_animes


# Example: Recommend animes similar to a given anime UID
uid = 4224  # Replace with the actual UID
recommended_animes = recommend_anime(uid, animes, cosine_sim)

# Save the DataFrame as well (optional, in case it's needed in app.py)
animes.to_csv('animes_with_tags.csv', index=False)
