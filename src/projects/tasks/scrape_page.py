import logging
import requests
import time
from bs4 import BeautifulSoup
from celery import shared_task
from django.conf import settings
from urllib.parse import urlparse
import time

@shared_task()
def scrape_page(page_id, url):
    data = {}
    start_time = time.time()
    try:
        # Use Crawl4AI to crawl the page and print URLs, title, and description

        CRAWL4AI_URL = getattr(settings, "CRAWL4AI_URL", "http://crawl4ai:11235")

        # Initialize default values
        title = "No title found"
        description = None
        urls = []
        crawl4ai_payload = {
            "urls": [url],
            "crawler_config": {
                "type": "CrawlerRunConfig", 
                "params": {
                    "stream": False,
                    "cache_mode": "bypass",
                }
            },
            "browser_config": {
                "type": "BrowserConfig",
                "params": {
                    "headless": True
                }
            }
        }
        
        # Retry mechanism for requests.post
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                crawl4ai_response = requests.post(
                    f"{CRAWL4AI_URL}/crawl",
                    json=crawl4ai_payload,
                    timeout=30,
                )
                
                # Check if we got a 500 error
                if crawl4ai_response.status_code == 500:
                    if attempt < max_retries - 1:  # Don't sleep on the last attempt
                        logging.warning(f"Attempt {attempt + 1} failed with 500 error, retrying in 2 seconds...")
                        time.sleep(2)
                        continue
                    else:
                        crawl4ai_response.raise_for_status()  # This will raise the 500 error
                
                # If we get here, the request succeeded or failed with a non-500 error
                crawl4ai_response.raise_for_status()
                break  # Success, exit the retry loop
                
            except requests.exceptions.HTTPError as e:
                if crawl4ai_response.status_code == 500 and attempt < max_retries - 1:
                    logging.warning(f"Attempt {attempt + 1} failed with 500 error, retrying in 2 seconds...")
                    time.sleep(2)
                    continue
                else:
                    raise  # Re-raise for non-500 errors or final attempt
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    logging.warning(f"Attempt {attempt + 1} failed with network error, retrying in 2 seconds...")
                    time.sleep(2)
                    continue
                else:
                    raise  # Re-raise on final attempt
        
        crawl4ai_data = crawl4ai_response.json()
        
        # crawl4ai_data should contain results for each URL
        if crawl4ai_data.get("success") and crawl4ai_data.get("results"):
            result = crawl4ai_data["results"][0]  # Get first result
            print("Crawl4AI Result:")
            print("URL:", result.get("url"))
            
            # Extract title and description
            title = result.get("metadata", {}).get("title") or "No title found"
            description = result.get("metadata", {}).get("description")
            
            print("Title:", title)
            print("Description:", description)
            
            # Define file extensions to ignore (images, pdfs, etc.)
            IGNORE_EXTENSIONS = (
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp',
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                '.zip', '.rar', '.tar', '.gz', '.mp3', '.mp4', '.avi', '.mov', '.wmv',
                '.css', '.js', '.ico', '.xml', '.txt',
                '.tex', '.py', '.bx2', '.tar.bz2'
            )
            
            def is_file_url(link_url):
                """Check if URL points to a file we want to ignore"""
                if not link_url:
                    return True
                
                # Parse the URL and get the path
                parsed = urlparse(link_url)
                path = parsed.path.lower()
                
                # Check if path ends with any ignored extension
                return any(path.endswith(ext) for ext in IGNORE_EXTENSIONS)
            
            # Filter internal links to exclude files
            internal_links = result.get("links", {}).get("internal", [])
            urls = []
            seen_urls = set()
            
            for link in internal_links:
                href = link.get("href")
                if href and not is_file_url(href):
                    # Remove fragment and query params for deduplication
                    parsed_href = urlparse(href)
                    clean_url = f"{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}"
                    
                    # Skip root path and duplicates
                    if parsed_href.path != "/" and clean_url not in seen_urls:
                        urls.append(href)
                        seen_urls.add(clean_url)
            
            print("Filtered URLs:", urls)

            data = {
                'title': title,
                'description': description,
                'urls': urls,
                'http_status': result.get("status_code"),
                'redirected_url': result.get("redirected_url"),
                'duration': time.time() - start_time,
            }
        else:
            raise Exception("No results from Crawl4AI")
    except Exception as e:
        data = {
            'http_status': 0,
            'error': str(e),
            'duration': time.time() - start_time,
        }
        logging.error(f"Error scraping the page: {e}")
    finally:
        try:
            response = requests.post(f'{settings.BACKEND_URL}/api/save_scaping/{settings.SECRET_KEY}/{page_id}/', json=data)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Error sending the result to the backend: {e}")
