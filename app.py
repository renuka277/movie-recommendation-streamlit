import pickle
import pandas as pd
import streamlit as st
import requests
import time
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ODZhOWExMWU3ZTM4OWZjYmVkYjgzNDVjN2YyM2RhMiIsIm5iZiI6MTc2NTcyOTc5NC45MzYsInN1YiI6IjY5M2VlNjAyM2U3MDg0YzNiZmFlY2NkZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.uS3TVM6FAuoUgDbnH0aNU6aqnLLiK5duNJV0SX4qQPo",
        "accept": "application/json"
    }

    for _ in range(3):  # retry 3 times
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('poster_path'):
                    return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        except:
            time.sleep(0.3)

    return "https://via.placeholder.com/300x450?text=No+Poster"
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie.append(movies.iloc[i[0]].title)

    return recommended_movie,recommended_movie_posters
st.header('Movie Recommendation System')
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies= pd.DataFrame(movies_dict)
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vectors)
selected_movie_name= st.selectbox(
    "Enter the Movie",
    movies['title'].values
)
if st.button('Recommended'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        if posters[0] is not None:
            st.image(posters[0])
        else:
            st.text("Poster not available")

    with col2:
        st.text(names[1])
        if posters[1] is not None:
            st.image(posters[1])
        else:
            st.text("Poster not available")

    with col3:
        st.text(names[2])
        if posters[2] is not None:
            st.image(posters[2])
        else:
            st.text("Poster not available")

    with col4:
        st.text(names[3])
        if posters[3] is not None:
            st.image(posters[3])
        else:
            st.text("Poster not available")

    with col5:
        st.text(names[4])
        if posters[4] is not None:
            st.image(posters[4])
        else:
            st.text("Poster not available")
