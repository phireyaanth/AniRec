from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Enable CORS so frontend can communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change this to frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load preprocessed anime dataset
animes = pd.read_csv('AnimesCleaned.csv')
animes_updated = pd.read_csv('animes_updated.csv')  # For fetching titles & UIDs

# Load precomputed models
with open('tfidf_matrix.pkl', 'rb') as f:
    tfidf_matrix = pickle.load(f)
cosine_sim = np.load('cosine_sim.npy')

# Define Pydantic model for request validation
class AnimeRequest(BaseModel):
    uid: int  # Expects a single UID as input

# Recommendation function
def recommend_anime(uid: int):
    try:
        idx = animes.index[animes['uid'] == uid].tolist()[0]
    except IndexError:
        return {"error": f"No anime found with UID {uid}"}

    # Get similarity scores and sort
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 recommendations

    # Get recommended anime indices
    anime_indices = [i[0] for i in sim_scores]

    # Retrieve recommended animes
    recommended_animes = animes_updated.loc[animes_updated['uid'].isin(animes.iloc[anime_indices]['uid'])]

    # Filter out "Hentai"
    recommended_animes = recommended_animes[~recommended_animes['genre'].apply(lambda x: 'Hentai' in x)]

    # Return only anime titles
    return {"recommended_titles": recommended_animes['title'].tolist()}

# FastAPI endpoint for recommendations
@app.post("/recommend")
def get_recommendations(request: AnimeRequest):
    return recommend_anime(request.uid)

# Run FastAPI using: uvicorn app:app --reload
