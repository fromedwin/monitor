# app_name/tasks.py
from celery import shared_task
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image
from io import BytesIO

@shared_task()
def fetch_favicon(pk, url):
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

        largest_favicon = None
        largest_size = (0, 0)

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
                print(f"Error fetching or processing {favicon_url}: {e}")

        if largest_favicon:
            print(f"Largest favicon found: {largest_favicon['url']} ({largest_favicon['width']}x{largest_favicon['height']})")
        else:
            print("No favicon found.")

        from projects.models import Project

        # Fetch the content of the favicon
        response = requests.get(largest_favicon['url'])
        response.raise_for_status()  # Ensure the request was successful

        # Wrap the content in a BytesIO object
        favicon_content = BytesIO(response.content)

        # Get the Project instance
        project = Project.objects.get(pk=pk)

        # Save the favicon to the project's ImageField or FileField
        project.favicon.save(largest_favicon['url'].split('/')[-1], favicon_content)

    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
