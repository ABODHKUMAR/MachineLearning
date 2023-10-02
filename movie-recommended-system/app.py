import pickle
import streamlit as st
import pandas as pd
import requests
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    # st.text(data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    for j in recommended_movie_names:
        print(j)
        print("cnt\n")
    return recommended_movie_names,recommended_movie_posters

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')

similarity = pickle.load(open('similarity.pkl','rb'))

# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Split the columns dynamically based on the number of recommendations
    num_recommendations = len(recommended_movie_names)
    num_columns = 5  # You can adjust this as needed

    # Calculate the number of rows needed
    num_rows = (num_recommendations - 1) // num_columns + 1

    # Loop through recommendations and display them in columns
    for i in range(num_rows):
        # st.write(f"Row {i + 1}")
        current_columns = st.columns(num_columns)

        for j in range(num_columns):
            index = i * num_columns + j
            if index < num_recommendations:
                current_column = current_columns[j]
                current_column.text(recommended_movie_names[index])
                current_column.image(recommended_movie_posters[index])




