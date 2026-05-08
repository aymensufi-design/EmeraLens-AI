import pandas as pd

def get_recommendations(movie_name):
    try:
        # Data load karein
        movies = pd.read_csv('movies.csv')
        ratings = pd.read_csv('ratings.csv')
        
        # 1. Smart Search Logic: Case-insensitive search
        match = movies[movies['title'].str.contains(movie_name, case=False, na=False)]
        
        # Agar exact match na mile, toh pehla word pakad ke search karein
        if match.empty:
            first_word = movie_name.split()[0]
            match = movies[movies['title'].str.contains(first_word, case=False, na=False)]
            
        # Agar phir bhi kuch na mile
        if match.empty:
            return ["Movie not found in database! Try another name."]
        
        # Pehli matching movie ki ID lein
        movie_id = match.iloc[0]['movieId']
        movie_title = match.iloc[0]['title']
        
        # 2. Collaborative Filtering:
        # Un users ko dhoondho jinhone ye movie dekhi hai
        similar_users = ratings[ratings['movieId'] == movie_id]['userId'].unique()
        
        # Un users ki dekhi hui saari movies ka data nikalna
        similar_user_movies = ratings[ratings['userId'].isin(similar_users)]
        
        # Top 6 movies recommend karna jo sabse zyada baar dekhi gayi hain
        recommendations = (similar_user_movies[similar_user_movies['movieId'] != movie_id]
                          .groupby('movieId')['rating']
                          .count()
                          .sort_values(ascending=False)
                          .head(6))
        
        # Movie IDs ko Titles mein convert karna
        result = movies[movies['movieId'].isin(recommendations.index)]['title'].tolist()
        
        return result if result else ["No similar recommendations found."]

    except Exception as e:
        return [f"Error: {str(e)}"]