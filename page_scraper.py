# region : IMPORTS
import os
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
# endregion : IMPORTS

# region : EXTRATEUR PAGE PAR PAGE
def scrape_page(url: str, output_folder: str = "markdown") -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Compatible; MySEOBot/1.0)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    if "text/html" not in response.headers.get("Content-Type", ""):
        raise ValueError(f"Le contenu récupéré n'est pas du HTML")

    soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")

    # Nettoyage RAG (Retrait des menus, scripts, styles et bas de page)
    for tag in soup(["script", "style", "nav", "footer", "header", "meta", "link"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title else "Page sans titre"

    content = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "code", "pre"]):
        if tag.name == "code" and tag.parent.name == "pre":
            continue

        text = tag.get_text(separator=" ", strip=True)
        if not text:
            continue

        if tag.name == "h1":
            content.append(f"# {text}")
        elif tag.name == "h2":
            content.append(f"## {text}")
        elif tag.name == "h3":
            content.append(f"### {text}")
        elif tag.name == "h4":
            content.append(f"#### {text}")
        elif tag.name == "pre":
            lines = text.split("\n")
            if len(text.split()) < 3 or (len(lines) == 1 and len(text) > 200):
                continue
            if not any(c in text for c in ["{", "(", "$", "`", "/"]):
                continue
            content.append(f"```\n{text}\n```")
        elif tag.name == "code":
            if len(text.split()) > 2:
                content.append(f"`{text}`")
        else:
            content.append(text)

    markdown = f"# {title}\n\nSource: {url}\n\n" + "\n\n".join(content)

    # Création du nom sécurisé de fichier
    parsed = urlparse(url)
    path = parsed.netloc + parsed.path
    filename = path.replace("/", "_").strip("_") + ".md"

    os.makedirs(output_folder, exist_ok=True)
    filepath = os.path.join(output_folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)

    return filepath
# endregion : EXTRATEUR PAGE PAR PAGE

# region : TRAITEMENT DE MASSE
def scrape_multiple_urls(urls, output_folder, status_callback=None, progress_callback=None):
    success = 0
    errors = 0
    total = len(urls)
    
    for index, url in enumerate(urls, start=1):
        try:
            scrape_page(url, output_folder=output_folder)
            success += 1
            if status_callback:
                status_callback(f"✅ [{index}/{total}] Converti : {url}")
        except Exception as e:
            errors += 1
            if status_callback:
                status_callback(f"❌ [{index}/{total}] Échec sur {url} ({str(e)})")
                
        if progress_callback:
            progress_callback(index, total)
            
    return success, errors
# endregion : TRAITEMENT DE MASSE