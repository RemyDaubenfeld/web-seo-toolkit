# region : IMPORTS
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
# endregion : IMPORTS

# region: DATA INITIALIZATION
def init_data(url, status, soup):
    parsed = urlparse(url)
    url = f"{parsed.scheme}://{parsed.netloc}/"

    title = soup.title.string.strip() if soup.title else "Missing"

    data = {
        "url": url,
        "status": status,
        "title": title,
        "meta_desc": "Missing",
        "h1_count": 0,
        "h2_count": 0,
        "h3_count": 0,
        "img_without_alt": 0,
        "robots_txt": False,
        "sitemap_xml": False,
        "sitemap_url": None,
        "errors": []
    }

    if status != 200:
        data["errors"].append(f"Incorrect HTTP status: {status}")

    if title == "Missing":
        data["errors"].append("Missing title tag")

    return data
# endregion: DATA INITIALIZATION

# region : SCANS
def meta_scan(soup, data):
    meta_desc = soup.find("meta", attrs={'name': 'description'})
    if meta_desc:
        data["meta_desc"] = meta_desc.get("content")
    else:
        data["meta_desc"] = "Missing"
        data["errors"].append("Missing meta description")

def title_scan(soup, data):
    data["h1_count"] = len(soup.find_all("h1"))
    data["h2_count"] = len(soup.find_all("h2"))
    data["h3_count"] = len(soup.find_all("h3"))

    if data["h1_count"] == 0:
        data["errors"].append("No H1 found")
    elif data["h1_count"] > 1:
        data["errors"].append(f"{data['h1_count']} H1 tags found — only one is recommended")

def img_scan(soup, data):
    images = soup.find_all('img')
    for img in images:
        if not img.get("alt"):
            data["img_without_alt"] += 1
    if data["img_without_alt"] > 0:
        data["errors"].append(f"{data['img_without_alt']} image(s) missing alt attribute")

def robots_scan(url, data):
    try:
        url_robots = urljoin(url, "robots.txt")
        response_robots = requests.get(url_robots, timeout=5)
        if response_robots.status_code == 200 and "User-agent" in response_robots.text:
            data["robots_txt"] = True
        else:
            data["errors"].append("Missing robots.txt")
    except:
        pass

def sitemap_scan(url, data):
    try:
        sitemap_path = urljoin(url, "sitemap.xml")
        response_sitemap = requests.get(sitemap_path, timeout=5)
        if response_sitemap.status_code == 200:
            data["sitemap_xml"] = True
            data["sitemap_url"] = sitemap_path
        else:
            data["errors"].append("Missing sitemap.xml")
    except:
        pass
# endregion : SCANS

# region : SEO ANALYSIS
def seo_analysis(url):
    try:
        response = requests.get(url, timeout=10)
        status = response.status_code
        soup = BeautifulSoup(response.text, 'html.parser')

        data = init_data(url, status, soup)

        meta_scan(soup, data)
        title_scan(soup, data)
        img_scan(soup, data)
        robots_scan(url, data)
        sitemap_scan(url, data)

        return data
    except Exception as e:
        return {"url": url, "error": str(e)}
# endregion : SEO ANALYSIS

# region : REPORT OUTPUT
def print_report(data):
    print("\nSEO Analysis:", data["url"])
    print("Status:", "✅" if data["status"] == 200 else "❌", data["status"])
    print("Title:", "✅" if data["title"] != "Missing" else "❌")
    print("Meta description:", "✅" if data["meta_desc"] != "Missing" else "❌")
    print("H1:", "✅" if data["h1_count"] == 1 else "❌", f"{data['h1_count']} found")
    print("Images without alt:", "✅" if data["img_without_alt"] == 0 else "❌", f"{data['img_without_alt']} image(s) missing alt")
    print("Robots.txt:", "✅" if data["robots_txt"] else "❌")
    print("Sitemap.xml:", "✅" if data["sitemap_xml"] else "❌")

    if len(data["errors"]) == 0:
        print("\n✅ No SEO issues detected")
    else:
        print(f"\n❌ {len(data['errors'])} issue(s) detected:")
        for error in data["errors"]:
            print("-", error)
# endregion : REPORT OUTPUT

# region : MAIN FUNCTION
def run_analysis(url):
    data = seo_analysis(url)
    return data
# endregion : MAIN FUNCTION