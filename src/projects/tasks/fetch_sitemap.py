from celery import shared_task
from django.conf import settings
from usp.tree import sitemap_tree_for_homepage
import time
from django.utils import timezone
from datetime import timedelta
from projects.models import Project
from projects.tasks.scrape_page import scrape_page
from logs.models import CeleryTaskLog
from django.shortcuts import get_object_or_404
from projects.models import Pages

@shared_task()
def fetch_sitemap(pk, url):
    start_time = time.time()
    tree = sitemap_tree_for_homepage(url)

    urls = [page.url for page in tree.all_pages()]
    duration = time.time() - start_time


    # Get performance to update
    project = get_object_or_404(Project, id=pk)

    sitemap_last_edited = timezone.now()

    # Only keep urls which have the same domain as the project url
    project_domain = project.url.split('/')[2]
    urls = [url for url in urls if project_domain in url]

    # Update sitemap_last_edited to pause fetching until deprecated
    project.sitemap_last_edited = sitemap_last_edited
    project.save()

    # If no urls from sitemap, we create a page for the project url
    if len(urls) == 0:
        page, created = Pages.objects.get_or_create(project=project, url=project.url)
        scrape_page.delay(page.pk, page.url)
    else:
        # Add project URL in list of pages to scrape but ignore same url if sitemap contains tailslash
        isProjectUrlSlashTailed = project.url.endswith('/')
        if isProjectUrlSlashTailed and project.url[:-1] not in urls and project.url not in urls:
            urls.append(project.url) # Add project url to the list of pages

        if not isProjectUrlSlashTailed and f'{project.url}/' not in urls and project.url not in urls:
            urls.append(project.url) # Add project url to the list of pages
        
        # Create new pages
        Pages.objects.bulk_create(
            [
                Pages(project=project, url=url, sitemap_last_seen=sitemap_last_edited) for url in urls
            ],
            ignore_conflicts=True  # This avoids inserting rows that violate uniqueness constraints
        )
        # Update existing pages data
        Pages.objects.filter(project=project, url__in=urls).update(sitemap_last_seen=sitemap_last_edited)

        # Send scraping request for all pages
        pages = Pages.objects.filter(sitemap_last_seen=sitemap_last_edited, project=project)
        for page in pages:
            scrape_page.delay(page.pk, page.url)

    # Send scraping request for all pages not in sitemap which were triggered on creation
    pages = Pages.objects.filter(sitemap_last_seen__isnull=True, project=project)
    for page in pages:
        page.sitemap_last_seen = sitemap_last_edited
        page.save()
        scrape_page.delay(page.pk, page.url)


    # Save log about sitemap task
    CeleryTaskLog.objects.create(
        project=project,
        task_name='sitemap_task',
        duration=timedelta(seconds=duration) if duration else None,
    )
