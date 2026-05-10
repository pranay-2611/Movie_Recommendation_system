import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------
# LOAD DATASETS
# ---------------------------------------------------

movies = pd.read_csv("Dataset/tmdb_5000_movies.csv")
credits = pd.read_csv("Dataset/tmdb_5000_credits.csv")

# ---------------------------------------------------
# MERGE DATASETS
# ---------------------------------------------------

movies = movies.merge(credits, on='title')

# ---------------------------------------------------
# SELECT REQUIRED COLUMNS
# ---------------------------------------------------

movies = movies[[
    'movie_id',
    'title',
    'overview',
    'genres',
    'keywords',
    'cast',
    'crew'
]]

# ---------------------------------------------------
# REMOVE NULL VALUES
# ---------------------------------------------------

movies.dropna(inplace=True)

# ---------------------------------------------------
# CONVERT FUNCTION
# ---------------------------------------------------

def convert(text):

    L = []

    for i in ast.literal_eval(text):
        L.append(i['name'])

    return L

# ---------------------------------------------------
# EXTRACT GENRES AND KEYWORDS
# ---------------------------------------------------

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# ---------------------------------------------------
# EXTRACT TOP 3 CAST MEMBERS
# ---------------------------------------------------

def convert_cast(text):

    L = []
    counter = 0

    for i in ast.literal_eval(text):

        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break

    return L

movies['cast'] = movies['cast'].apply(convert_cast)

# ---------------------------------------------------
# FETCH DIRECTOR NAME
# ---------------------------------------------------

def fetch_director(text):

    L = []

    for i in ast.literal_eval(text):

        if i['job'] == 'Director':
            L.append(i['name'])
            break

    return L

movies['crew'] = movies['crew'].apply(fetch_director)

# ---------------------------------------------------
# CONVERT OVERVIEW INTO LIST
# ---------------------------------------------------

movies['overview'] = movies['overview'].apply(lambda x: x.split())

# ---------------------------------------------------
# REMOVE SPACES
# ---------------------------------------------------

movies['genres'] = movies['genres'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['keywords'] = movies['keywords'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['cast'] = movies['cast'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

movies['crew'] = movies['crew'].apply(
    lambda x: [i.replace(" ", "") for i in x]
)

# ---------------------------------------------------
# CREATE TAGS
# ---------------------------------------------------

movies['tags'] = (
    movies['overview'] +
    movies['genres'] +
    movies['keywords'] +
    movies['cast'] +
    movies['crew']
)

# ---------------------------------------------------
# NEW DATAFRAME
# ---------------------------------------------------

new_df = movies[['movie_id', 'title', 'tags']]

# ---------------------------------------------------
# CONVERT LIST TO STRING
# ---------------------------------------------------

new_df['tags'] = new_df['tags'].apply(
    lambda x: " ".join(x)
)

# ---------------------------------------------------
# LOWERCASE
# ---------------------------------------------------

new_df['tags'] = new_df['tags'].apply(
    lambda x: x.lower()
)

# ---------------------------------------------------
# TEXT VECTORIZATION
# ---------------------------------------------------

cv = CountVectorizer(
    max_features=5000,
    stop_words='english'
)

vectors = cv.fit_transform(new_df['tags']).toarray()

# ---------------------------------------------------
# COSINE SIMILARITY
# ---------------------------------------------------

similarity = cosine_similarity(vectors)

# ---------------------------------------------------
# MOVIE LIST
# ---------------------------------------------------

movie_list = new_df['title'].values

# ---------------------------------------------------
# RECOMMENDATION FUNCTION
# ---------------------------------------------------

def recommend_movies(movie_name):

    movie_index = new_df[
        new_df['title'] == movie_name
    ].index[0]

    distances = similarity[movie_index]

    movie_list_sorted = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for movie in movie_list_sorted:

        recommended_movies.append(
            new_df.iloc[movie[0]].title
        )

    return recommended_movies
