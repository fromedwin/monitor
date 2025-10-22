import logging
import base64
import requests
import time
from celery import shared_task, current_app
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image
from io import BytesIO
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from projects.models import Project
from .models import Favicon

@shared_task()
def fetch_favicon(pk, url):
    largest_favicon = None
    largest_size = (0, 0)
    largest_content = None
    duration = None
    start_time = time.time()
    try:
        # Get the HTML content of the webpage
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all possible favicon links
        icon_links = soup.find_all("link", rel=lambda rel: rel and 'icon' in rel.lower())

        favicons = []
        for icon in icon_links:
            if 'href' in icon.attrs:
                favicon_url = urljoin(url, icon['href'])
                favicons.append(favicon_url)

        # Add default favicon location as a fallback
        parsed_url = urlparse(url)
        default_favicon = f"{parsed_url.scheme}://{parsed_url.netloc}/favicon.ico"
        favicons.append(default_favicon)


        # If one url in favicon end with svg we keep this ad largest favicon
        for favicon_url in favicons:
            try:
                # Fetch the favicon image
                favicon_response = requests.get(favicon_url, timeout=10)
                favicon_response.raise_for_status()

                # Open the image and get its size
                image = Image.open(BytesIO(favicon_response.content))
                width, height = image.size

                # Update the largest favicon if this one is larger
                if width * height > largest_size[0] * largest_size[1]:
                    largest_size = (width, height)
                    largest_favicon = {
                        'url': favicon_url,
                        'width': width,
                        'height': height,
                    }

            except Exception as e:
                logging.info(f"Error fetching or processing {favicon_url}: {e}")

        # If no image found, we try to get the first svg found
        if not largest_favicon:
            if any(favicon_url.endswith('.svg') for favicon_url in favicons):
                largest_favicon = {
                    'url': next(favicon_url for favicon_url in favicons if favicon_url.endswith('.svg')),
                    'width': 0,
                    'height': 0,
                }

        if largest_favicon:
            logging.debug(f"Largest favicon found: {largest_favicon['url']} ({largest_favicon['width']}x{largest_favicon['height']})")
            # Fetch the content of the favicon
            response = requests.get(largest_favicon['url'])
            response.raise_for_status()  # Ensure the request was successful

            # Wrap the content in a BytesIO object
            largest_content = base64.b64encode(response.content).decode('utf-8')

    except Exception as e:
        logging.error(f"Error fetching the webpage: {e}")
    finally:
        duration = time.time() - start_time
        try:
            response = requests.post(f'{settings.BACKEND_URL}/api/save_favicon/{settings.SECRET_KEY}/{pk}/', json={
                'favicon_url': largest_favicon['url'] if largest_favicon else None,
                'favicon_content': largest_content,
                'duration': duration,
            })
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Error sending the result to the backend: {e}")
        logging.info(f"Task completed for project {pk}")



@shared_task(bind=True)
def queue_deprecated_favicons(self):

    # Revoke all tasks with the same name currently queued
    inspector = current_app.control.inspect()
    active_tasks = inspector.active()
    reserved_tasks = inspector.reserved()

    task_name = self.name
    task_id = self.request.id

    # Helper function to revoke tasks
    def revoke_tasks(tasks):
        for worker, tasks_list in tasks.items():
            for task in tasks_list:
                if task['name'] == task_name and task['id'] != task_id:
                    current_app.control.revoke(task['id'], terminate=True)
                    print(f"Revoked task {task['id']} on worker {worker}")

    # Revoke tasks that are currently active
    if active_tasks:
        revoke_tasks(active_tasks)

    # Revoke tasks that are reserved (queued but not started)
    if reserved_tasks:
        revoke_tasks(reserved_tasks)

    six_hours_ago = timezone.now() - timedelta(hours=settings.TIMINGS['FAVICON_INTERVAL_HOURS'])
    projects = Project.objects.filter(
        Q(favicon_details__last_edited__lt=six_hours_ago) | Q(favicon_details__isnull=True)
    )
    
    for project in projects:
        favicon, created = Favicon.objects.get_or_create(
            project=project,
            defaults={'task_status': 'PENDING'}
        )
        if not created:
            favicon.task_status = 'PENDING'
            favicon.save()

    projects = [{'id': project.pk, 'url': project.url} for project in projects]

    logging.info(f'Found {len(list(projects))} projects to refresh favicon.')
    for project in projects:
        fetch_favicon.delay(project.get('id'), project.get('url'))
