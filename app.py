import streamlit as st
import pickle
import pandas as pd

# Load the pickle files
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('🎬 Movie Recommendation System')

selected_movie = st.selectbox(
    'Type or select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    # Fetch index of the selected movie
    movie_index = movies[movies['title'] == selected_movie].index[0]
    distances = similarity[movie_index]
    index_list = list(enumerate(distances))
    
    # Sort and get top 5 similar movies (excluding the movie itself)
    similar_movies = sorted(index_list, reverse=True, key=lambda x: x[1])[1:6]
    
    st.write("### Recommended Movies for You:")
    for i, value in similar_movies:
        st.write(f"- {movies.iloc[i]['title']}")
