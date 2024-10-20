# src/projects/tasks/fetch_favicon.py
from celery import shared_task
from usp.tree import sitemap_tree_for_homepage
from performances.models import Performance
import logging
from projects.models import Project

@shared_task()
def fetch_sitemap(pk, url):

    project_id = pk
    tree = sitemap_tree_for_homepage(url)
    # for page in tree.all_pages():
    #     print(page)

    # print(f'Found {len(list(tree.all_pages()))} pages in sitemap.')
    project = Project.objects.get(pk=pk)
    if len(list(tree.all_pages())) < 300:
        logging.info(f'Project {url} has less than 300 pages in sitemap.')
        Performance.objects.bulk_create(
            [
                Performance(project=project, url=page.url) for page in tree.all_pages()
            ],
            ignore_conflicts=True  # This avoids inserting rows that violate uniqueness constraints
        )
    else:
        logging.warning(f'Project {url} has more than 300 pages in sitemap, ignored for now.')
