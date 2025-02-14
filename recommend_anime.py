import pandas as pd
import numpy as np
import pickle

# Load preprocessed anime dataset
animes = pd.read_csv('AnimesCleaned.csv')
animes_updated = pd.read_csv('animes_updated.csv')  # For fetching titles and UIDs

# Load precomputed TF-IDF matrix and cosine similarity matrix
with open('tfidf_matrix.pkl', 'rb') as f:
    tfidf_matrix = pickle.load(f)
cosine_sim = np.load('cosine_sim.npy')

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

    # Print recommendations
    if not recommended_animes.empty:
        print("Recommended Animes (excluding Hentai):")
        for idx, row in recommended_animes.iterrows():
            print(f"UID: {row['uid']}, Title: {row['title']}")
    else:
        print("No recommendations available (all recommended animes had the 'Hentai' tag).")

    return recommended_animes

# Example usage
if __name__ == "__main__":
    uid = 4224  # Replace with a real UID
    recommended_animes = recommend_anime(uid, animes, cosine_sim)