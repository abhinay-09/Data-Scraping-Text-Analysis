import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

def extract_data(url_id, url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting title from the article
        title_element = soup.find('h1', class_=['tdb-title-text', 'entry-title'])
        title = title_element.get_text(strip=True) if title_element else 'No Title Found'

        # Extracting content from the article
        article_body = soup.find('div', class_='td-post-content')
        if not article_body:
            print(f"Article content not found for URL_ID: {url_id}")
            # Create an empty file if the article content is not found
            with open(os.path.join('articles', f'{url_id}.txt'), 'w', encoding='utf-8'):
                pass
            return None

        article = ""
        for element in article_body.find_all(['p', 'li', 'h2']):
            article += element.get_text(separator=' ', strip=True) + " "

        # Saving the article text to a file
        with open(os.path.join('articles', f'{url_id}.txt'), 'w', encoding='utf-8') as file:
            file.write(title + "\n" + article.strip())

        return title, article.strip()
    except Exception as e:
        print(f"Failed to extract {url} for URL_ID {url_id}: {e}")
        # Create an empty file if an error occurs
        with open(os.path.join('articles', f'{url_id}.txt'), 'w', encoding='utf-8'):
            pass
        return None

def main():
    # Read input Excel file
    data = pd.read_excel("input.xlsx")

    # Ensure the 'articles' directory exists
    if not os.path.exists('articles'):
        os.makedirs('articles')

    for index, row in data.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
        extract_data(url_id, url)

if __name__ == "__main__":
    main()
