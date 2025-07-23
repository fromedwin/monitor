import logging
import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.conf import settings
from urllib.parse import urlparse

@shared_task()
def scrape_page(page_id, url):
    data = {}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Step 2: Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
            
            # Step 3: Extract the page title
            title = soup.title.string if soup.title else "No title found"
            logging.info(f"Page Title: {title}")
            
            # Step 4: Extract the meta description
            description_tag = soup.find("meta", attrs={"name": "description"})
            description = description_tag["content"] if description_tag else None
            logging.info(f"Meta Description: {description}")

            # get all urls in the page with same domain
            # 'netloc' is the network location part of a URL, which typically includes the domain name and (optionally) the port number.
            # For example, in 'https://example.com:8080/path', netloc is 'example.com:8080'.
            base_url = url
            base_parsed = urlparse(base_url)
            base_domain = base_parsed.netloc
            base_scheme = base_parsed.scheme

            urls = []
            # Define file extensions to ignore (images, pdfs, etc.)
            IGNORE_EXTENSIONS = (
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp',
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                '.zip', '.rar', '.tar', '.gz', '.mp3', '.mp4', '.avi', '.mov', '.wmv'
            )

            seen_urls = set()
            for a in soup.find_all('a', href=True):
                href = a['href'].strip()
                # Ignore mailto, javascript, tel, and empty/invalid links
                if not href or href.startswith(('mailto:', 'javascript:', 'tel:', '#')):
                    continue
                # Ignore links to files with unwanted extensions
                if any(href.lower().split('?', 1)[0].endswith(ext) for ext in IGNORE_EXTENSIONS):
                    continue
                parsed_href = urlparse(href)
                # Remove query params and fragment
                clean_path = parsed_href.path
                # Only consider links with a path
                if not clean_path:
                    continue
                # Ignore root path "/"
                if clean_path == "/":
                    continue
                # Rebuild the absolute URL (scheme://domain/path)
                if not parsed_href.netloc:
                    # Relative URL, make absolute
                    abs_url = f"{base_scheme}://{base_domain}{clean_path}"
                elif parsed_href.netloc == base_domain:
                    # Absolute URL, same domain
                    abs_url = f"{base_scheme}://{base_domain}{clean_path}"
                else:
                    continue  # Skip external domains

                # Check again for file extension after cleaning
                if not any(abs_url.lower().endswith(ext) for ext in IGNORE_EXTENSIONS):
                    # Ignore duplicate URLs
                    if abs_url not in seen_urls:
                        urls.append(abs_url)
                        seen_urls.add(abs_url)
            logging.info(f"Urls: {urls}")
            data = {
                'title': title,
                'description': description,
                'urls': urls,
                'http_status': response.status_code
            }
        else:
            data = {
                'http_status': response.status_code
            }
            logging.error(f"Failed to fetch the webpage. Status code: {response.status_code}")
    except Exception as e:
        data = {
            'http_status': 0,
            'error': str(e)
        }
        logging.error(f"Error scraping the page: {e}")
    finally:
        try:
            response = requests.post(f'{settings.BACKEND_URL}/api/save_scaping/{settings.SECRET_KEY}/{page_id}/', json=data)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Error sending the result to the backend: {e}")
