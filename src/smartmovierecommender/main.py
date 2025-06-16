import pandas as pd 
import logging 
import argparse
from sklearn.metrics.pairwise import cosine_similarity
import os
print(os.getcwd())

from smartmovierecommender.utils.combining_data import movie_combiner, get_movie_rec, preprocess_movies, load_and_save_csv
from smartmovierecommender.calculation.cosine_sim import convert_duration, convert_ratings, cosine_sim, cosine_max, convert_to_title



logging.basicConfig(
    level=logging.INFO,
    filename='logs.txt',
    filemode='w', 
    format='%(asctime)s - %(levelname)s - %(message)s'
)



logging.info("Starting to score Main file")


def main(movie_title):
    """
    Main function to load the data, process the movies, and perform cosine similarity
    Args: the movie title inputted
    Return: one
    """
    # below loads the data from the google link
    additional_data = load_and_save_csv()
    #opens the function to get the dataset 

    print(os.getcwd())
    #movies = preprocess_movies(additional_data[0])
    #movies = preprocess_movies("../data/processed-data/file_1.csv")
    movies = preprocess_movies("data/processed-data/file_1.csv")

    #does the cosine sim and gets the top 5 recs 
    recs = get_movie_rec(movies,movie_title)
    if recs.empty:
        logging.info("No recommendations found.")
    else:
        print("\nTop Recommendations:")
        logging.info("\nTop Recommendations:")
        for i, row in recs.iterrows():
            print(f"{row['Title']} (Similarity: {row['Similarity']:.2f})")
            logging.info(f"{row['Title']} (Similarity: {row['Similarity']:.2f})")


 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Movie_recommender_script")
    parser.add_argument("-cs", "--to_cosine_score", action="store_true", help="Flag to gemini score")
    parser.add_argument("-t", required=True, help="Title of Movie")
    
    args = parser.parse_args()
    main(
        movie_title=args.t
    )
    
    logging.info('Scoring is completed')  
    logging.shutdown()  
    