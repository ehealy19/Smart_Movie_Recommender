import json
import google.generativeai as genai
import os
import pandas as pd
import time
import re
import csv
import chardet
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY_GEMINI = os.environ.get("gemapi")

genai.configure(api_key=API_KEY_GEMINI)

def chat_with_gemini(prompt, retries=3, delay=5):
    """
    Helper function to chat with Gemini API
    Args: the prompt for Gemini, the number of retries allowed, the time delay between retries
    Returns: None
    """
    for attempt in range(retries):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-8b-latest")
            response = model.generate_content(prompt)
            # Extract the response content
            answer = response.candidates[0].content.parts[0].text
            return answer

        except Exception as e:
            if "429" in str(e):  # Rate limit error
                print(f"Attempt {attempt + 1}: Rate limit hit. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"An error occurred: {e}")
                return None
    print("Exceeded retry limit.")
    return None

def parse_response(response):
    """
    Updated function to clean and parse the response
    Args: the response from Gemini
    Returns: the cleaned response
    """
    try:
        # Remove any common code block markers
        cleaned_response = re.sub(r"```json|```", "", response).strip()

        # Use regex to extract JSON-like content
        json_match = re.search(r"\{.*\}", cleaned_response, re.DOTALL)
        if json_match:
            json_content = json_match.group(0)
            parsed_data = json.loads(json_content)
            return parsed_data
        else:
            print("No JSON content found in the response.")
            return None

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None

    
def process_movies():
    """
    Main function to collect the Gemini responses
    Args: None
    Returns: the list of movies with the Gemini genre ratings
    """
    all_movies = []  # List to store cleaned job data
    
    for filename in os.listdir('Data'):
        if not filename.endswith('.json'):
            print(f"Skipping non-JSON file: {filename}")
            continue
        input_file = os.path.join('Data', filename)
        print(f"processing file: {filename}")
        
        with open(input_file, 'r', encoding='Windows-1252') as file:
            movie_data = json.load(file)

            movie = movie_data[62]
            title = movie.get("Title")
            prompt = f"""
                You are an expert in rating films. Can you please give me a score of how much
                each film from this list: "{title}" fits into each of these categories. Please score from 0-1, where 0 is the 
                film does not fit the category at all and 1 is that the film perfectly fits the category 
                (the score don't have to add to 1 and the precision is 0.01). Base these results on your 
                understanding of the film from IMDb and google description of the film. DO NOT OUTPUT NAN - give 
                a score for each movie, for each genre. Please output these scores 
                for each film directly as a JSON response (ie like this: 
                [{{'Mission: Impossible 2': {{'action': 0.95, 'adventure': 0.9,}}}}]). 
                Here are the categories:

                - action
                - adventure
                - animation
                - art
                - biography
                - comedy
                - crime
                - dark comedy
                - documentary
                - drama
                - epic
                - family
                - fantasy
                - fiction
                - history
                - historical drama
                - horror
                - music
                - musical
                - mystery
                - noir
                - romance
                - romantic comedy
                - science fiction
                - sport
                - thriller
                - war
                - western
                """

        # Get the response from Gemini API
            response = chat_with_gemini(prompt)
            time.sleep(1)
            if response:
                parsed_data = parse_response(response)
                if parsed_data:
                    all_movies.append(parsed_data)
                else:
                    print(f"Failed to parse response")
            else:
                print("No reponse from API")

    return all_movies

# Execute the job processing function and save to a DataFrame
cleaned_movies = process_movies()
print(cleaned_movies)
if cleaned_movies:
    flattened_data = []
    for movie in cleaned_movies:
        for film_name, genres in movie.items():
            # Create a new dictionary with the film name and genres
            flattened_entry = {'movie': film_name}
            if isinstance(genres, dict):
                flattened_entry.update(genres)  # Add genre scores to the dictionary
            else:
                print(f"Unexpected data format for genres: {genres}")
            flattened_data.append(flattened_entry)
    df = pd.DataFrame(flattened_data)
    print(df)
    print("Checking for missing values in the DataFrame:")
    print(df.isnull().sum())

    # Fill NaN values with 0
    df.fillna(0, inplace=True)

    output_path = "../../../data/output_data/cleaned_movies62.csv"
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Data saved to {output_path}")
else:
    print("No data to save")