# region : IMPORTS
import os
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
# endregion : IMPORTS

class SEOCrawler:
    # region : INITIALIZATION
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.to_crawl = [self.base_url]
        self.site_data = []
    # endregion : INITIALIZATION

    # region : LINK VALIDATION
    def is_valid_internal_link(self, url):
        parsed = urlparse(url)
        return (parsed.netloc == self.domain or parsed.netloc == "") and \
               not any(url.lower().endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.zip', '.css', '.js', '.svg', '.json'])
    # endregion : LINK VALIDATION

    # region : URL DISCOVERY
    def get_url_list(self, update_callback=None):
        """
        Recursively crawls the site to collect all valid internal URLs.
        """
        discovered_urls = set()

        while self.to_crawl:
            url = self.to_crawl.pop(0)
            if url in self.visited_urls:
                continue

            try:
                if update_callback:
                    update_callback(f"🔍 Link found: {url}")

                headers = {'User-Agent': 'Mozilla/5.0 (Compatible; MySEOBot/1.0)'}
                response = requests.get(url, headers=headers, timeout=10)
                self.visited_urls.add(url)

                if "text/html" in response.headers.get("Content-Type", ""):
                    discovered_urls.add(url)
                    soup = BeautifulSoup(response.content, "html.parser")

                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(url, href).split('#')[0].split('?')[0].rstrip('/')

                        if self.is_valid_internal_link(full_url) and full_url not in self.visited_urls:
                            if full_url not in self.to_crawl:
                                self.to_crawl.append(full_url)

            except Exception as e:
                if update_callback:
                    update_callback(f"⚠️ Could not index {url}: {str(e)}")

        return list(discovered_urls)
    # endregion : URL DISCOVERY

    # region : FULL SEO CRAWL
    def crawl(self):
        while self.to_crawl:
            url = self.to_crawl.pop(0)
            if url in self.visited_urls:
                continue

            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Compatible; MySEOBot/1.0)'}
                response = requests.get(url, headers=headers, timeout=10)
                self.visited_urls.add(url)

                if response.status_code == 200 and "text/html" in response.headers.get("Content-Type", ""):
                    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

                    self.site_data.append({
                        "url": url,
                        "title": soup.title.string.strip() if soup.title else "MISSING",
                        "h1": soup.find('h1').get_text().strip() if soup.find('h1') else "MISSING",
                        "soup": soup
                    })

                    for a_tag in soup.find_all('a', href=True):
                        link = urljoin(url, a_tag['href']).split('#')[0].rstrip('/')
                        if self.is_valid_internal_link(link) and link not in self.visited_urls:
                            if link not in self.to_crawl:
                                self.to_crawl.append(link)
                time.sleep(0.1)
            except Exception as e:
                print(f"Error on {url}: {e}")
    # endregion : FULL SEO CRAWL