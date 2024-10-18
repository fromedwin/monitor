# src/projects/tasks/fetch_favicon.py
from celery import shared_task

from usp.tree import sitemap_tree_for_homepage

@shared_task()
def fetch_sitemap(pk, url):
    tree = sitemap_tree_for_homepage(url)
    for page in tree.all_pages():
        print(page)

    print(f'Found {len(list(tree.all_pages()))} pages in sitemap.')
