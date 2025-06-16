import os
import json
import re
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


if not os.path.exists('../../../data/scraped_data'):
    os.makedirs('../../../data/scraped_data')


def save_to_json(data, chunk_num):
    """
    Saves the movie information to a JSON file
    Args: the list of movie information to save, the index of the filename
    Returns: outputs the movie to JSON into data folder following naming conventions
    """
    filename = f"../../../data/scraped_data/movies_chunk_{chunk_num}.json"
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    logging.info(f"Saving {len(data)} movies to {filename}")

def extract_movie_data(raw_text):
    """
    Extracts the movie information for each film from the returned API information
    Args: the raw text giving the movie information
    Returns: the title, year, duration, MPAA rating, IMDb rating, number of rating, and description for each movie
    """
    movies = []
    raw_movies = raw_text.split('\n\n')  
    
    for movie_text in raw_movies:
        movie = {}

        title = re.match(r"^\d+\.\s*(.+?)\n", movie_text)  
        if title:
            movie["Title"] = title.group(1).strip()

        year = re.search(r"\b(\d{4})\b(?!\s*\.)", movie_text)  
        if year:
            movie["Year"] = year.group(1)

        duration = re.search(r"(\d+h\s\d+m|\d+h|\d+m)", movie_text)
        if duration:
            movie["Duration"] = duration.group(0)

        rated = re.search(r"(G|PG|PG-13|R|NC-17|Unrated)", movie_text)
        if rated:
            movie["Rated"] = rated.group(0)

        imdb_rating = re.search(r"\b\d\.\d{1,2}\b", movie_text)
        if imdb_rating:
            movie["IMDB Rating"] = imdb_rating.group(0)

        num_ratings = re.search(r"\(\d{1,3}(?:[.,]\d{3})*(?:K|M)?\)", movie_text)
        if num_ratings:
            movie["Number of Ratings"] = num_ratings.group(0)[1:-1]  

        rate = re.search(r"\b\d{1,3}%\b", movie_text)
        if rate:
            movie["Rate"] = rate.group(0)

        description = re.split(r"\d{4}", movie_text)  
        if description:
            movie["Description"] = description[-1].strip()

        if "Title" in movie and "Year" in movie:
            movies.append(movie)

    return movies

def process_raw_data(raw_text):
    """
    Combines the processing of the movie text data and saving to JSON
    Args: the text information of the movie
    """
    chunk_num = 1
    data = []
    movies = extract_movie_data(raw_text)
    for i, movie in enumerate(movies):
        data.append(movie)
        if len(data) >= 1000:
            save_to_json(data, chunk_num)
            data = [] 
            chunk_num += 1
    if data:
        save_to_json(data, chunk_num)


def scraper(url):
    """
    Scraper function to get the raw movie information using API
    Args: the URL to scrape from
    Returns: the raw text information about the movie
    """
    options = Options()
    options.headless = False  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    logging.info("Driver started.")
    time.sleep(3)
    data = []
    chunk_num = 1  

    try:
        while True:
            html = driver.page_source
            logging.info("scraping")
            movies = driver.find_elements(By.CSS_SELECTOR, "div.ipc-metadata-list-summary-item__c")
            for movie in movies:
                movie_text = movie.text.strip()
                data.append(movie_text)
    
            process_raw_data('\n\n'.join(data))

            try:
                wait = WebDriverWait(driver, 20)  
                button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ipc-see-more__text")))
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1) 
                logging.info("Found 250 more button")
                driver.execute_script("arguments[0].click();", button)
                time.sleep(3)  
            except Exception as e:
                logging.error("No more entries :", e)
                break
    
    except Exception as e:
        logging.error("error :", e)

    driver.quit()
    logging.info("Driver closed.")

url = 'https://www.imdb.com/search/title/?title_type=feature&countries=US&languages=en&count=250'
scraper(url)
