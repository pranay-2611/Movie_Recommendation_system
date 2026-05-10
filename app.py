import streamlit as st
import pandas as pd
import ast
import zipfile

from model import recommend_movies, movie_list

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
with zipfile.Zipfile("Dataset.zip") as z:
    movies_data = pd.read_csv(z.open("Dataset/tmdb_5000_movies.csv"))
    credits_data = pd.read_csv(z.open("Dataset/tmdb_5000_credits.csv"))

movies_data = movies_data.merge(credits_data, on="title")

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Movie Recommendation",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

page_style = """
<style>

/* Background */

[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1440404653325-ab127d49abc1?q=80&w=2070&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Transparent Header */

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Main Box */

.main-box {
    background: rgba(0,0,0,0.65);
    backdrop-filter: blur(10px);
    padding: 40px;
    border-radius: 20px;
    margin-top: 30px;
}

/* Title */

.title {
    text-align: center;
    color: white;
    font-size: 60px;
    font-weight: bold;
}

/* Subtitle */

.subtitle {
    text-align: center;
    color: #dddddd;
    font-size: 22px;
    margin-bottom: 40px;
}

/* Buttons */

.stButton>button {
    width: 100%;
    background-color: #e50914;
    color: white;
    font-size: 22px;
    border-radius: 10px;
    padding: 12px;
    border: none;
    font-weight: bold;
}

/* Button Hover */

.stButton>button:hover {
    background-color: #ff1f1f;
}

/* Selectbox */

.stSelectbox label {
    color: white !important;
    font-size: 22px;
    font-weight: bold;
}

/* Result Box */

.result-box {
    background: rgba(255,255,255,0.10);
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    color: white;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0px 0px 10px rgba(0,0,0,0.4);
}

</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

if st.session_state.page == "home":

    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.markdown(
        '<div class="title">🎬 AI Movie Recommendation System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Find movies similar to your favorites using Artificial Intelligence</div>',
        unsafe_allow_html=True
    )

    selected_movie = st.selectbox(
        "Choose Your Favorite Movie",
        movie_list
    )

    if st.button("🍿 Show Recommendations"):

        st.session_state.selected_movie = selected_movie
        st.session_state.page = "results"

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# RESULTS PAGE
# ---------------------------------------------------

elif st.session_state.page == "results":

    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.markdown(
        '<div class="title">🍿 Recommended Movies</div>',
        unsafe_allow_html=True
    )

    recommendations = recommend_movies(
        st.session_state.selected_movie
    )

    for movie in recommendations:

        movie_info = movies_data[
            movies_data['title'] == movie
        ].iloc[0]

        # ---------------------------------------------------
        # FETCH CAST
        # ---------------------------------------------------

        cast_names = []

        try:
            cast_list = ast.literal_eval(movie_info['cast'])

            for actor in cast_list[:5]:
                cast_names.append(actor['name'])

        except:
            pass

        cast = ", ".join(cast_names)

        # ---------------------------------------------------
        # FETCH DIRECTOR
        # ---------------------------------------------------

        director = "Not Available"

        try:
            crew_list = ast.literal_eval(movie_info['crew'])

            for member in crew_list:

                if member['job'] == 'Director':
                    director = member['name']
                    break

        except:
            pass

        # ---------------------------------------------------
        # DISPLAY RESULT
        # ---------------------------------------------------

        st.markdown(
            f"""
            <div class="result-box">

            <h2>🎬 {movie}</h2>

            <p><b>⭐ Top Cast:</b> {cast}</p>

            <p><b>🎥 Director:</b> {director}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    if st.button("⬅ Back to Home"):

        st.session_state.page = "home"

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
