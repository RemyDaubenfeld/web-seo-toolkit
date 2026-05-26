# region : IMPORTS
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from urllib.parse import urlparse
import requests
# endregion : IMPORTS

# region : ROBOTS.TXT FETCHER
def download_robots_txt(base_url):
    """
    Fetches the robots.txt file from the root of the given site.
    """
    parsed_url = urlparse(base_url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Compatible; MySEOBot/1.0)'}
        response = requests.get(robots_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            return f"# File not found on server (HTTP status: {response.status_code})"
    except Exception as e:
        return f"# Could not fetch robots.txt: {str(e)}"
# endregion : ROBOTS.TXT FETCHER

# region : SITEMAP XML GENERATOR
def generate_xml_sitemap(url_list, filepath):
    """
    Takes a list of URLs and generates a clean, indented sitemap.xml file.
    """
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for url in url_list:
        url_node = ET.SubElement(urlset, "url")
        ET.SubElement(url_node, "loc").text = url

    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="   ")

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
# endregion : SITEMAP XML GENERATOR