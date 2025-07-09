# --- FILE 1: scrape_to_csv.py ---
# Scrape IMDb data using Selenium and save to CSV

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
#import streamlit as st

# Initialize WebDriver
driver = webdriver.Chrome()
url = "https://www.imdb.com/search/title/?title_type=feature&genres=action,adventure,comedy,horror,romance"
driver.get(url)
time.sleep(3)

# Initialize lists
titles, ratings, votings, durations,storylines = [], [], [], [], []

# Get all movie elements
movie_items = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li')
for movie_item in movie_items:
    try:
        # Extract the movie title
        title = movie_item.find_element(By.XPATH, './div/div/div/div[1]/div[2]/div[1]/a/h3').text

        # Extract the movie rating
        rating = movie_item.find_element(By.XPATH, './div/div/div/div[1]/div[2]/span/div/span/span[1]').text

        # Extract the number of votes
        voting = movie_item.find_element(By.XPATH, './div/div/div/div[1]/div[2]/span/div/span/span[2]').text

        # Extract the movie duration
        duration = movie_item.find_element(By.XPATH, './div/div/div/div[1]/div[2]/div[2]/span[2]').text

        # Extract the storyline (plot summary)
        storyline = movie_item.find_element(By.XPATH, './div/div/div/div[2]/div/div').text
        # Append the data to the lists
        titles.append(title)
        ratings.append(rating)
        votings.append(voting)
        durations.append(duration)
        storylines.append(storyline)
    
    except Exception as e:
        # If any element is not found, skip this movie and print an error message
        print(f"Error extracting data for a movie: {e}")
        continue

# Create a DataFrame using the extracted data
df = pd.DataFrame({
    'Title': titles,
    'Rating': ratings,
    'Votes': votings,
    'Duration': durations,
    'Storyline': storylines  # Add the storyline column
})

# # Save the DataFrame to a CSV file (optional)
#df.to_csv('imdb_movies_2024.csv', index=False)
df.to_csv(r"C:\Users\Ravi\Desktop\Desktop\Sample program\Test\imdb_movies_2024.csv", index=False)

# Close the browser
#driver.quit()
#st=df