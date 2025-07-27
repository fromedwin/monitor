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

            # Use Crawl4AI to crawl the page and print URLs, title, and description

            CRAWL4AI_URL = getattr(settings, "CRAWL4AI_URL", "http://crawl4ai:11235")

            # Initialize default values
            title = "No title found"
            description = None
            urls = []

            try:
                crawl4ai_payload = {
                    "urls": [url],
                    "crawler_config": {
                        "type": "CrawlerRunConfig", 
                        "params": {
                            "stream": False,
                            "cache_mode": "bypass"
                        }
                    },
                    "browser_config": {
                        "type": "BrowserConfig",
                        "params": {
                            "headless": True
                        }
                    }
                }
                crawl4ai_response = requests.post(
                    f"{CRAWL4AI_URL}/crawl",
                    json=crawl4ai_payload,
                    timeout=30,
                )
                crawl4ai_response.raise_for_status()
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
                    
            except Exception as e:
                print(f"Error calling Crawl4AI: {e}")

            data = {
                'title': title,
                'description': description,
                'urls': urls,
                'http_status': result.get("status_code"),
                'redirected_url': result.get("redirected_url"),
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
