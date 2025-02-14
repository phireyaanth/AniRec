import pandas as pd
from Anime_DS_updated import animes
from Anime_DS_updated import animes_import

if __name__ == "__main__":
    print("This is the Final DF for the Recommendation system"+ "\n" + "\n")
    print(animes[['title', 'synopsis', 'genre', 'Relative Length', 'Years', 'tags']].head())

org_anime = pd.read_csv('animes_updated.csv')


# Sample DataFrame (replace this with your actual DataFrame)
# animes = pd.read_csv('your_anime_file.csv')

# Function to retrieve data using UID
def get_title_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['title'].values[0]
    else:
        return None

def get_synopsis_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['synopsis'].values[0]
    else:
        return None

def get_genre_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['genre'].values[0]
    else:
        return None

def get_aired_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['aired'].values[0]
    else:
        return None

def get_episodes_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['episodes'].values[0]
    else:
        return None

def get_popularity_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['popularity'].values[0]
    else:
        return None

def get_ranked_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['ranked'].values[0]
    else:
        return None

def get_score_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['score'].values[0]
    else:
        return None

def get_img_url_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['img_url'].values[0]
    else:
        return None

def get_link_by_uid(df, uid):
    row = df[df['uid'] == uid]
    if not row.empty:
        return row['link'].values[0]
    else:
        return None

# Example usage:
uid = 18397  # Replace with the actual UID you want to retrieve
if __name__ == "__main__":
    print("Title:", get_title_by_uid(org_anime, uid))
    print("Synopsis:", get_synopsis_by_uid(org_anime, uid))
    print("Genre:", get_genre_by_uid(org_anime, uid))
    print("Aired:", get_aired_by_uid(org_anime, uid))
    print("Episodes:", get_episodes_by_uid(org_anime, uid))
    print("Popularity:", get_popularity_by_uid(org_anime, uid))
    print("Ranked:", get_ranked_by_uid(org_anime, uid))
    print("Score:", get_score_by_uid(org_anime, uid))
    print("Image URL:", get_img_url_by_uid(org_anime, uid))
    print("Link:", get_link_by_uid(org_anime, uid))

    # Assuming 'df' is your DataFrame
    unique_genres = animes_import['genre'].unique()
    print(unique_genres)







