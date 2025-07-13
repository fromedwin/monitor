import logging
import requests
from celery import shared_task
from django.conf import settings
from usp.tree import sitemap_tree_for_homepage
import time

@shared_task()
def fetch_sitemap(pk, url):
    start_time = time.time()
    tree = sitemap_tree_for_homepage(url)
    try:
        response = requests.post(f'{settings.BACKEND_URL}/api/save_sitemap/{settings.SECRET_KEY}/{pk}/', json={
            'urls': [page.url for page in tree.all_pages()],
            'duration': time.time() - start_time,
        })
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Error sending the result to the backend: {e}")
