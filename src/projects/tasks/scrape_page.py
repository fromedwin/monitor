import logging
import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.conf import settings

@shared_task()
def scrape_page(page_id, url):
    response = requests.get(url)
    if response.status_code == 200:
        # Step 2: Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        
        # Step 3: Extract the page title
        title = soup.title.string if soup.title else "No title found"
        logging.info(f"Page Title: {title}")
        
        # Step 4: Extract the meta description
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"] if description_tag else "No description meta found"
        logging.info(f"Meta Description: {description}")

        data = {
            'title': title,
            'description': description,
        }
        try:
            response = requests.post(f'{settings.BACKEND_URL}/api/save_scaping/{settings.SECRET_KEY}/{page_id}/', json=data)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Error sending the result to the backend: {e}")
    else:
        logging.error(f"Failed to fetch the webpage. Status code: {response.status_code}")
