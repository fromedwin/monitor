from celery import shared_task
from projects.utils.scrape_url import scrape_url

import json
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from projects.models import Pages, PageLink
from logs.models import CeleryTaskLog
from django.db import transaction
         
@shared_task()
def scrape_page(page_id, url):
    title, description, urls, http_status, redirected_url, duration = scrape_url(url)
    # Use django settings secret_key to authenticate django worker

    # Get performance to update
    page = get_object_or_404(Pages, id=page_id)

    page.http_status = http_status if http_status else 0
    if redirected_url and http_status == 301:
        page.save()
        to_page, created = Pages.objects.get_or_create(
            url=redirected_url,
            project=page.project,
        )
        PageLink.objects.filter(from_page=page).delete()
        # Create the link (no need for get_or_create since we deleted all links above)
        PageLink.objects.create(
            from_page=page,
            to_page=to_page
        )

    elif http_status == 404:
        page.save()
        PageLink.objects.filter(from_page=page).delete()
    else:
        page.title = title
        page.description = description
        page.scraping_last_seen = timezone.now()
        page.save()

        # Use transaction to ensure atomicity and prevent database locks
        with transaction.atomic():
            # Delete all existing outbound links from this page first (clean slate)
            PageLink.objects.filter(from_page=page).delete()
            
            # Create new links for all discovered URLs
            for url in urls:
                # Prevent a page from linking to itself
                # Ignore if the URL is the same as the current page, or if it doesn't start with the full domain (scheme + netloc)
                from urllib.parse import urlparse
                page_parsed = urlparse(page.url)
                url_parsed = urlparse(url)
                page_base = f"{page_parsed.scheme}://{page_parsed.netloc}"
                url_base = f"{url_parsed.scheme}://{url_parsed.netloc}"
                if url == page.url or url_base != page_base:
                    continue
                # Get or create the target page within the same project
                to_page, created = Pages.objects.get_or_create(
                    url=url,
                    project=page.project,
                )

                # Create the link (no need for get_or_create since we deleted all links above)
                PageLink.objects.create(
                    from_page=page,
                    to_page=to_page
                )
    
    # Save log about sitemap task
    log = CeleryTaskLog.objects.create(
        project=page.project,
        task_name='scraping_task',
        duration=timedelta(seconds=duration) if duration else None,
    )

    page.scraping_task_log = log
    page.save()

