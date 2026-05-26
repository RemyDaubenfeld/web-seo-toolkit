# region : IMPORTATION DES LIBRAIRIES
import requests #Bibliothèque HTTP simple qui permet d'envoyer des requêtes HTTP/1.1
from bs4 import BeautifulSoup #Bibliothèque de parsing HTML qui facilite l'extraction de données à partir de fichiers HTML et XML
import pandas as pd #Bibliothèque de manipulation de données qui offre des structures de données flexibles et puissantes pour l'analyse de données
from urllib.parse import urljoin, urlparse #Bibliothèque pour manipuler les URLs
# endregion : IMPORTATION DES LIBRAIRIES

# region: INITIALISATION DES DONNEES
def init_data(url, status, soup):

    # Extraction de la racine du site
    parsed = urlparse(url) # On parse l'URL pour extraire le schéma et le domaine
    url = f"{parsed.scheme}://{parsed.netloc}/"

    title = soup.title.string.strip() if soup.title else "Manquant"

    data = {
        "url": url,
        "status": status,
        "title": title,
        "meta_desc": "Manquant",
        "h1_count": 0,
        "h2_count": 0,
        "h3_count": 0,
        "img_sans_alt": 0,
        "robots_txt": False,
        "sitemap_xml": False,
        "sitemap_url": None,
        "errors": []
    }

    if status != 200:
        data["errors"].append(f"Status HTTP incorrect : {status}")

    if title == "Manquant":
        data["errors"].append("Title manquant")

    return data
# endregion: INITIALISATION DES DONNEES

# region : SCANS
#Scan de la meta description
def meta_scan(soup, data):
        meta_desc = soup.find("meta", attrs={'name': 'description'})
        if meta_desc:
            data["meta_desc"] = meta_desc.get("content")
        else:
            data["meta_desc"] = "Manquant"
            data["errors"].append("Meta description manquante")

#Scan des titres
def title_scan(soup, data):
    data["h1_count"] = len(soup.find_all("h1"))
    data["h2_count"] = len(soup.find_all("h2"))
    data["h3_count"] = len(soup.find_all("h3"))

    if data["h1_count"] == 0: 
        data["errors"].append("Aucun H1 trouvé")
    elif data["h1_count"] > 1:
        data["errors"].append(f"{data['h1_count']} H1 trouvés, il est recommandé d'en avoir un seul")  

#Scan des images sans alt
def img_scan(soup, data):
        images = soup.find_all('img')
        for img in images:
            if not img.get("alt"):
                data["img_sans_alt"] += 1
        if data["img_sans_alt"] > 0:
            data["errors"].append(f"{data['img_sans_alt']} images sans alt")

# Vérification de l'existence d'un fichier robots.txt
def robots_scan(url, data):
    try:
        url_robots = urljoin(url, "robots.txt") # On construit l'URL complète du fichier robots.txt à partir de la racine
        response_robots = requests.get(url_robots, timeout=5)
        if response_robots.status_code == 200 and "User-agent" in response_robots.text:
            data["robots_txt"] = True
        else:
            data["errors"].append("Robots.txt manquant")
    except: 
        pass

# Vérification de l'existence d'un fichier sitemap.xml
def sitemap_scan(url, data):
    try:
        sitemap_path = urljoin(url, "sitemap.xml")
        response_sitemap = requests.get(sitemap_path, timeout=5)
        if response_sitemap.status_code == 200:
            data["sitemap_xml"] = True
            data["sitemap_url"] = sitemap_path # On stocke l'URL du sitemap trouvé pour référence si besoin de crawler le sitemap plus tard
        else:
            data["errors"].append("Sitemap.xml manquant")
    except: 
        pass
# endregion : SCANS

# region : ANALYSE SEO
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
# endregion : ANALYSE SEO

# region : AFFICHAGE DU RAPPORT
def print_report(data):

    print("\nAnalyse SEO :", data["url"])

    print("Status :", "✅" if data["status"] == 200 else "❌", data["status"])
    print("Title :", "✅" if data["title"] != "Manquant" else "❌")
    print("Meta description :", "✅" if data["meta_desc"] != "Manquant" else "❌")
    print("H1 :", "✅" if data["h1_count"] == 1 else "❌", f"{data['h1_count']} trouvé(s)")
    print("Images sans alt :", "✅" if data["img_sans_alt"] == 0 else "❌", f"{data['img_sans_alt']} image(s) sans alt")
    print("Robots.txt :", "✅" if data["robots_txt"] else "❌")
    print("Sitemap.xml :", "✅" if data["sitemap_xml"] else "❌")

    if len(data["errors"]) == 0:
        print("\n✅ Aucun problème SEO détecté")
    else:
        print(f"\n❌ {len(data['errors'])} problème(s) détecté(s) :")
        for error in data["errors"]:
            print("-", error)
# endregion : AFFICHAGE DU RAPPORT

# region : FONCTION PRINCIPALE
def run_analysis(url):
    data = seo_analysis(url)
    #print_report(data)
    return data
# endregion : FONCTION PRINCIPALE