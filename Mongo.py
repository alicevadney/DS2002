import pymongo

# Import necessary libraries
from pymongo import MongoClient
import pprint

# Replace with your MongoDB Atlas connection string (password redacted)
connection_string = "mongodb+srv://epm2wu:<*password*>@cluster0.gm9g0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(connection_string)

# Access the sample_mflix database and the movies collection
db = client['sample_mflix']
collection = db['movies']

# Write a query to find the first movie that has the genre "Action".
action_movie = collection.find({"genres": "Action"}).limit(1)
pprint.pprint(action_movie)

# Write a query to find all movies released after the year 2000 (Return the first 5 results).
movies_after_2000 = collection.find({"year": {"$gt": 2000}}).limit(5)
for movie in movies_after_2000:
    pprint.pprint(movie)

# Write a query to find all movies where the IMDb rating is greater than 8.5 (Return the first 5 results).
best_rated_movies = collection.find({"imdb.rating": {"$gt": 8.5}}).limit(5)

# Write a query to find all movies where the genre contains both "Action" and "Adventure".
action_adventure_movies = collection.find({"genres": {"$all": ["Action", "Adventure"]}}).limit(5)

# Write a query to find all movies where the genre is "Comedy" and sort them by IMDb rating in descending order (Return the first 5 results).
sorted_comedy_movies = collection.find({"genres": "Comedy"}).sort("imdb.rating", -
1).limit(5)

# Write a query to find all movies where the genre is "Drama" and sort them by release year in ascending order (Return the first 5 results)
sorted_drama_movies = collection.find({"genres": "Drama"}).sort("year", 1).limit(5)

#Write an aggregation pipeline that calculates the  average IMDb rating for each genre (Return the top 5 genres).
avg_rating_by_genre = collection.aggregate([
    {"$unwind": "$genres"},
    {"$group": {"_id": "$genres", "avg_rating": {"$avg": "$imdb.rating"}}},
    {"$sort": {"avg_rating": -1}},
    {"$limit": 5}])

# Write an aggregation pipeline to find the top 5 directors by the average IMDb rating of their movies.
top_directors = collection.aggregate([
{"$group": {"_id": "$directors", "avg_rating": {"$avg": "$imdb.rating"}}},
    {"$sort": {"avg_rating": -1}},
    {"$limit": 5}])

# Write an aggregation pipeline to calculate the total number of movies released in each year (Sort the results by the year)
movies_per_year = collection.aggregate([{"$group": {"_id": "$year", "total_movies": {"$sum": 1}}},
                                        {"$sort": {"_id": 1}}])

# Write a query to update the IMDb rating of a movie with the title "The Godfather" to 9.5.
collection.update_godfather({"title": "The Godfather"}, {"$set": {"imdb.rating": 9.5}})


#Write a query to update all movies where the genre is "Horror" and set their IMDb rating to 6.0 if it is currently null.
collection.update_horror({"genres": "Horror", "imdb.rating": {"$exists": False}}, {"$set":
{"imdb.rating": 6.0}})

# Write a query to delete all movies that were released before the year 1950.
collection.delete_old({"year": {"$lt": 1950}})

# Ensure the title field is indexed for text search in MongoDB and write a query to search for movies that contain the word "love" in their title.
collection.create_index([("title", "text")])
love_movies = collection.find({"$text": {"$search": "love"}})

# Write a text search query to find movies where the word "war" appears in the title or plot, sorted by IMDb rating (Return only the top 5 results).
collection.create_index([("title", "text"), ("plot", "text")])
war_movies = collection.find({"$text": {"$search": "war"}}).sort("imdb.rating", -1).limit(5)
