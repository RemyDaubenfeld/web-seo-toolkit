> **[🇬🇧 English](README.md) | [🇫🇷 Français](README.fr.md)**

# 🕷️ Web Scraper & SEO Audit Toolkit

![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)

Une boîte à outils desktop locale pour l'audit SEO, la conversion de sites web en Markdown et la génération de sitemaps. Développée en Python avec Tkinter — sans cloud, sans télémétrie, 100% hors ligne.

---

## ✨ Fonctionnalités

- **📊 Audit SEO** — Analyse une URL pour détecter les problèmes SEO courants : title manquant, meta description, structure des H1, images sans `alt`, présence du `robots.txt` et du `sitemap.xml`. Les résultats sont exportés dans un rapport `.csv`.
- **📝 Conversion en Markdown** — Crawle un site entier et convertit chaque page HTML en fichier Markdown propre, débarrassé des scripts, styles, menus et pieds de page. Idéal pour les pipelines RAG ou l'archivage de documentation.
- **🌐 Génération Sitemap & Robots.txt** — Explore récursivement un site pour découvrir toutes les URLs internes, génère un `sitemap.xml` valide et sauvegarde une copie locale du `robots.txt`.

---

## 🚀 Démarrage

### Prérequis

- Python **3.11+**
- Un environnement graphique (requis pour l'interface Tkinter)

> **Note pour les utilisateurs Linux (Ubuntu/Mint/Debian) :** Les distributions Linux modernes implémentent la PEP 668, qui restreint les installations `pip` à l'échelle du système. Utilisez votre gestionnaire de paquets natif ou un environnement virtuel (voir les options ci-dessous).

---

### Installation

#### Option A — Installation rapide (système via APT, Linux uniquement)

```bash
sudo apt update && sudo apt install python3-pandas python3-bs4 python3-requests python3-tk -y
```

#### Option B — Installation propre (environnement virtuel, toutes plateformes)

1. Clonez ce dépôt ou téléchargez les fichiers sources.
2. Créez et activez un environnement virtuel :

```bash
python3 -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

> **⚠️ Paquets Windows uniquement :** `requirements.txt` inclut `winrt-*`, `sounddevice` et `vosk` qui sont spécifiques à Windows ou optionnels. Sur Linux/macOS, ignorez les erreurs pip pour ces paquets — le toolkit principal n'en dépend pas.

---

### Lancement

```bash
python3 main.py
```

Cela ouvre l'interface graphique de configuration depuis laquelle vous pouvez saisir une URL cible, choisir un dossier de sortie et sélectionner une action.

---

## 📁 Structure du projet

```
.
├── main.py              # Point d'entrée — interface Tkinter et routage des actions
├── seo_scanner.py       # Logique d'analyse SEO (page unique)
├── seo_crawler.py       # Crawler récursif de liens internes
├── page_scraper.py      # Convertisseur HTML vers Markdown
├── sitemap_manager.py   # Générateur de sitemap XML et récupération du robots.txt
├── data_manager.py      # Export CSV et gestion des logs
└── requirements.txt     # Dépendances Python
```

Les fichiers de sortie sont sauvegardés dans le dossier `data/` par défaut (configurable via l'interface) :

```
data/
├── csv/        # Rapports d'audit SEO
├── markdown/   # Pages converties en Markdown
├── sitemaps/   # Sitemaps générés et copies du robots.txt
└── logs/       # Logs d'exécution
```

---

## 🛠️ Développé avec

| Bibliothèque | Rôle |
|---|---|
| [Tkinter](https://docs.python.org/3/library/tkinter.html) | Interface graphique desktop native |
| [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) | Parsing HTML et extraction de contenu |
| [Requests](https://requests.readthedocs.io/) | Transactions HTTP synchrones |
| [Pandas](https://pandas.pydata.org/) | Compilation de DataFrames et export CSV |

---

## 🔒 Confidentialité & Sécurité

- **Traitement 100% local** — Aucune télémétrie, aucune API tierce, aucun stockage cloud. Tous vos crawls et contenus extraits restent sur votre machine.
- **En-tête User-Agent** — Toutes les requêtes HTTP s'identifient comme `MySEOBot/1.0`. Assurez-vous d'avoir l'autorisation de crawler vos sites cibles et que cela respecte leurs directives `robots.txt`.