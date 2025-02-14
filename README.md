Overview
This project is a content-based recommendation system designed to suggest the most relevant anime titles based on a given input anime. The system processes over 20,000 anime titles and provides personalized recommendations by analyzing various features like title, genre, synopsis, and episode count. The goal is to help users discover new anime based on their preferences efficiently and accurately.

Features
Content-based filtering: Uses TF-IDF vectorization and cosine similarity to find the most relevant anime titles.
Data preprocessing: Cleans and processes 7+ data columns (e.g., title, genre, synopsis, release date, episodes).
Personalized recommendations: Provides the top 10 most relevant recommendations based on the user's selected anime.
Filtering NSFW content: Excludes anime with inappropriate content to ensure high-quality recommendations.
Optimized performance: Caches matrices and similarity scores to improve response time.
Technologies Used
Languages: Python
Libraries: pandas, numpy, matplotlib, ast, re, scikit-learn
Machine Learning/NLP: TF-IDF vectorization, Cosine similarity
Tools: Jupyter Notebook, Conda environments
Setup & Installation
Clone the repository:

git clone <repository-url>
cd anime-recommendation-system
Set up a virtual environment:


conda create -n anime-env python=3.8
conda activate anime-env
Install required packages:


pip install pandas numpy matplotlib scikit-learn
Prepare the dataset:

Ensure the anime data is available in a CSV file (e.g., animes_updated.csv).
Place the dataset in the project directory.

Usage Example
python
Copy code
# Example: Recommend similar animes based on a given anime UID
uid = 4224  # Replace with your desired anime UID
recommended_animes = recommend_anime(uid, animes, cosine_sim)

print(recommended_animes)
Dataset Overview
The dataset contains over 20,000 anime titles and includes the following columns:

Title: Name of the anime
Genre: List of genres
Synopsis: Brief description of the plot
Aired: Release date
Episodes: Total number of episodes
Popularity & Score: User ratings
Relative Length: Categorized length (e.g., Mini, Average, Large)
Recommendation Logic
Data Preprocessing:

Cleans missing values in the synopsis, genres, and episode counts.
Converts genres into lists and tokenizes text features (title, synopsis).
Feature Extraction:

Uses TF-IDF vectorization to transform text data into numerical vectors.
Combines title, genre, synopsis, and other features into a "tags" column for analysis.
Similarity Calculation:

Cosine similarity measures the closeness between vectors to find similar anime titles.
The top 10 anime titles with the highest similarity scores are recommended.
Future Enhancements
User profiles: Allow users to save favorite anime and get personalized recommendations.
Advanced filtering: Include genre preferences or episode limits in the recommendation logic.
Web integration: Deploy the recommendation system as a web application using Flask or React.
Contributing
Feel free to fork the repository and submit a pull request for improvements or new features.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
Special thanks to the anime community and data providers for making this project possible by sharing their datasets.

Let me know if you need any further modifications!






