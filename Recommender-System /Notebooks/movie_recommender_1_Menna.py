import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader, Dataset, KNNBasic, accuracy
from surprise.model_selection import train_test_split


###### all my functions

def item_similarity(movieId, n):
    # Create a DataFrame using the values from 'movies_cosines_matrix' for the given movieId
    cosines_df = pd.DataFrame(movies_cosines_matrix[movieId])

    # Remove the row with the index matching the input movieId
    cosines_df = cosines_df[cosines_df.index != movieId]

    # Sort the cosine similarity values in descending order
    cosines_df = cosines_df.sort_values(by=movieId, ascending=False)

    # Find out the number of users who rated both the input movie and the other movies
    no_of_users_rated_both_movies = [sum((user_movie_matrix[movieId] > 0) & (user_movie_matrix[x] > 0)) for x in cosines_df.index]

    # Create a column for the number of users who rated both movies
    cosines_df['users_who_rated_both_movies'] = no_of_users_rated_both_movies

    # Remove recommendations that have less than 10 users who rated both movies
    cosines_df = cosines_df[cosines_df['users_who_rated_both_movies'] > 10]

    # Get the names and other information for the recommended movies
    top_n_cosine = (cosines_df
                            .head(n)
                            .reset_index()
                            .merge(df_1.drop_duplicates(subset='movieId'),
                                    on='movieId',
                                    how='left')
                            [movie_info_columns + [movieId, 'users_who_rated_both_movies']]
                            )

    return top_n_cosine


def n_predictions_for_user(testset, user_input, num_recommendations):
    filtered_testset = []

    # Loop through a big testset
    for row in testset:
        # Filter the ones with our user_id
        if row[0] == user_input:
            # Add the filtered ones to an empty list
            filtered_testset.append(row)

    # Do predictions on the filtered testset
    predictions = algo.test(filtered_testset)

    # Extract item ids and estimated ratings from predictions
    item_estimations = [(pred.iid, pred.est) for pred in predictions]

    # Sort item_estimations by estimated rating ('est') in descending order
    sorted_item_estimations = sorted(item_estimations, key=lambda x: x[1], reverse=True)[:num_recommendations]

    return sorted_item_estimations

##### end of all functions



# Load movies and ratings data
movies_df = pd.read_csv('movies.csv')  # Replace with the actual path to your movies.csv file
ratings_df = pd.read_csv('ratings.csv')  # Replace with the actual path to your ratings.csv file
rating_weight = 0.7
count_weight = 0.3
# Function for Popularity-Based Recommendations    
def popularity(ratings_df, movies_df):
    # Merge ratings_df and movies_df on 'movieId'
    df_1 = pd.merge(ratings_df, movies_df, on='movieId')

    # Group by 'movieId' and aggregate data
    test_df = df_1.groupby('movieId').agg({'rating': 'mean', 'userId': 'count'})

    # Scale the numeric columns (rating and userId)
    scaler = MinMaxScaler()
    test_df[['rating', 'userId']] = scaler.fit_transform(test_df[['rating', 'userId']])

    # Calculate weighted ratings
    test_df['book_rating_weighted'] = test_df['rating'] * rating_weight
    test_df['count_weighted'] = test_df['userId'] * count_weight
    test_df['final_rating'] = test_df['book_rating_weighted'] + test_df['count_weighted']

    # Sort by final_rating in descending order
    test_df = test_df.sort_values('final_rating', ascending=False)

    # Reset the index and merge with movie titles
    test_df = test_df.reset_index()
    output = test_df.merge(movies_df[['title', 'movieId']], how='left', on='movieId').drop_duplicates()

    return output

# Call the popularity function
popularity_recommendations = popularity(ratings_df, movies_df)

# Select specific columns from the DataFrame
selected_columns = popularity_recommendations[['movieId', 'title', 'final_rating']]

# Display the top 10 recommendations
top_10_recommendations = selected_columns.head(10)

# Streamlit UI
st.table(top_10_recommendations)




# Sidebar for Model Selection
model = st.selectbox("Pick Your Movie Magic Generator", ["Similar Movies", "Similar People Like You"])

# Create a dropdown menu for selecting a user ID
if model == "Similar Movies":
    user_input = st.text_input("Enter a Movie ID:")
elif model == "Similar People Like You":
    user_input = st.selectbox("Select a User ID", list(range(1, 611)))

# # Add a button to trigger the recommendation
# if st.button("Get Recommendations"):
#     # Call your recommendation function here with the selected user_input
#     recommendations = n_predictions_for_user(testset, user_input, num_recommendations)
    
#     # Display the recommendations
#     st.dataframe(recommendations)


# Number of Recommendations
num_recommendations = st.slider("Number of Recommendations", min_value=1, max_value=10, value=5)

# # Sample list of genres
# genres = [
#     "Crime|Drama",
#     "Comedy|Drama|Romance|War",
#     "Comedy|Crime|Drama|Thriller",
#     "Action|Sci-Fi|Thriller",
#     "Crime|Horror|Thriller",
#     "Action|Adventure|Sci-Fi",
#     "Action|Crime|Drama|Thriller",
#     "Drama|War",
#     "Action|Adventure|Sci-Fi",
#     "Crime|Mystery|Thriller",
# ]

# # Create a dropdown menu for selecting a genre
# selected_genre = st.selectbox("Select from the Top 10 Genre Selection", genres)

# # Display the selected genre
# st.write("You selected the genre:", selected_genre)

# Button to Generate Recommendations
if st.button("Get Recommendations"):
    if model == "Similar Movies":
        df_1 = pd.merge(ratings_df, movies_df, on='movieId')

        user_movie_matrix = pd.pivot_table(data=df_1,
                                          values='rating',
                                          index='userId',
                                          columns='movieId',
                                          fill_value=0)

        movies_cosines_matrix = pd.DataFrame(cosine_similarity(user_movie_matrix.T),
                                            columns=user_movie_matrix.columns,
                                            index=user_movie_matrix.columns)

        movie_info_columns = ['movieId', 'title']

        

        # Call the item_similarity function with user_input and num_recommendations
        recommendations = item_similarity(int(user_input), num_recommendations)

        st.header("Recommended Movies:")
        st.table(recommendations)

    elif model == "Similar People Like You":
        # Call your n_predictions_for_user function here
        
        reader = Reader(rating_scale=(1, 5))
        df_1 = pd.merge(ratings_df, movies_df, on='movieId')
        data = df_1[['userId', 'movieId', 'rating']]
        data = Dataset.load_from_df(data, reader)
        trainset, testset = train_test_split(data, test_size=0.2, random_state=142)
        
        sim_options = {
            'name': 'cosine',
            'user_based': True
        }

        full_train = data.build_full_trainset()
        algo = KNNBasic(sim_options=sim_options, min_k=3)
        algo.fit(full_train)
        testset = full_train.build_anti_testset()

        
        
        recommendations = n_predictions_for_user(testset, user_input, num_recommendations)
        filter_df = df_1[['title', 'genres', 'movieId']]
        result_df = pd.DataFrame(recommendations, columns=['iid', 'est']).merge(filter_df, how='left', left_on='iid', right_on='movieId').drop_duplicates()
        st.dataframe(result_df)
        

        
