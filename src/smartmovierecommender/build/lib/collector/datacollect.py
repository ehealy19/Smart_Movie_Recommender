#open api 
#import API key 
import requests
import json
import csv
import requests
from bs4 import BeautifulSoup


with open('/Users/rachnarawalpally/dsan5400-project/api_key.json') as f:
    keys = json.load(f)
API_KEY = keys['OMDb API']


#get top movies from wikipedia for the dataset 
def get_movie_titles_from_wikipedia(url):
    #fetch the web page content
    response = requests.get(url)
    
    #parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #find all tables in the page (looking specifically for the one that lists the movies)
    tables = soup.find_all('table', {'class': 'wikitable'})

    movie_titles = []

    #loop through the tables and extract movie titles
    for table in tables:
        #find all rows in the table
        rows = table.find_all('tr')
        
        for row in rows:
            #get all table data (td) in the row
            columns = row.find_all('td')
            
            if columns:
                #check if there is a title in the first column (typically the movie title)
                title_column = columns[0] 
                if title_column:
                    title = title_column.get_text(strip=True)
                    movie_titles.append(title)

    return movie_titles

#this is the code to run the above file
#need to input the url to wikipdeia with the list of movies
url = "https://en.wikipedia.org/wiki/List_of_American_films_of_2010"
movies = get_movie_titles_from_wikipedia(url)

#print movie titles, only get the top 350 films for the year 
movies_list = [movie_2010 for movie_2010 in movies[:10] if not movie_2010.isdigit()]
print(movies_list)


#list of movies 
movie_titles = movies_list


def fetch_movie_details(movie_titles, API_KEY):
    """
    Fetch movie details from the OMDB API.
    """
    movie_details = []

    for movie_title in movie_titles:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            movie_data = response.json()
            if movie_data['Response'] == 'True':
                movie_details.append({
                    "Title": movie_data.get('Title', 'N/A'),
                    "Year": movie_data.get('Year', 'N/A'),
                    "Duration": movie_data.get('Runtime', 'N/A'),
                    "Rated": movie_data.get('Rated', 'N/A'),
                    "IMDB Rating": movie_data.get('imdbRating', 'N/A'),
                    "Number of Ratings": movie_data.get('imdbVotes', 'N/A'),
                    "Description": movie_data.get('Plot', 'N/A'),
                })
            else:
                print(f"Movie not found: {movie_data['Error']}")
        else:
            print(f"Failed to fetch movie data for {movie_title}")

    return movie_details


def fetch_movie_details_imdb(movie_title):

    #Fetch movie details from the OMDB API
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
        response = requests.get(url)
        movie_data = response.json()
        if movie_data['Response'] == 'True':
            {
                    "Title": movie_data.get('Title', 'N/A'),
                    "Year": movie_data.get('Year', 'N/A'),
                    "Duration": movie_data.get('Runtime', 'N/A'),
                    "Rated": movie_data.get('Rated', 'N/A'),
                    "IMDB Rating": movie_data.get('imdbRating', 'N/A'),
                    "Number of Ratings": movie_data.get('imdbVotes', 'N/A'),
                    "Description": movie_data.get('Plot', 'N/A'),
                }
        else:
            print(f"Movie not found: {movie_data['Error']}")
            return None
