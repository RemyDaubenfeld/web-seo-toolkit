# region : IMPORTS
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from urllib.parse import urlparse
import requests
# endregion : IMPORTS

# region : EXTRACTION ROBOTS.TXT
def download_robots_txt(base_url):
    """
    Va chercher le fichier robots.txt à la racine du site fourni.
    """
    parsed_url = urlparse(base_url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Compatible; MySEOBot/1.0)'}
        response = requests.get(robots_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            return f"# Fichier introuvable sur le serveur (Code HTTP: {response.status_code})"
    except Exception as e:
        return f"# Impossible d'extraire le fichier robots.txt : {str(e)}"
# endregion : EXTRACTION ROBOTS.TXT

# region : GENERATION SITEMAP XML
def generate_xml_sitemap(url_list, filepath):
    """
    Prend une liste d'URLs et génère un fichier sitemap.xml propre et indenté.
    """
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for url in url_list:
        url_node = ET.SubElement(urlset, "url")
        ET.SubElement(url_node, "loc").text = url

    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="   ")

    # Assure que le dossier parent existe
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
# endregion : GENERATION SITEMAP XML