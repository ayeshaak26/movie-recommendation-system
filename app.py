import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")

st.title('🎬 Movie Recommendation System')
st.write("Find your next favorite film based on cast, crew, genre, and plot similarities.")

# Load the lightweight dataframes and text engine
movies = pickle.load(open('movie_list.pkl', 'rb'))
cv = pickle.load(open('cv.pkl', 'rb'))

# Calculate the similarity matrix live on the web server memory
@st.cache_data # This keeps the app incredibly fast by calculating it only once per session
def calculate_similarity():
    vectors = cv.transform(movies['tags']).toarray()
    return cosine_similarity(vectors)

similarity = calculate_similarity()

selected_movie = st.selectbox(
    'Type or select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Get Recommendations', type="primary"):
    movie_index = movies[movies['title'] == selected_movie].index[0]
    distances = similarity[movie_index]
    index_list = list(enumerate(distances))
    
    # Sort and slice out the top 5 similar items
    similar_movies = sorted(index_list, reverse=True, key=lambda x: x[1])[1:6]
    
    st.write("### 🍿 Recommended Movies for You:")
    for i, value in similar_movies:
        st.info(f"**{movies.iloc[i]['title']}**")
