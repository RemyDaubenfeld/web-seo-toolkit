> **[🇬🇧 English](README.md) | [🇫🇷 Français](README.fr.md)**

# 🕷️ Web Scraper & SEO Audit Toolkit

![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)

A local desktop toolkit for SEO auditing, website-to-Markdown conversion, and sitemap generation. Built with Python and Tkinter — no cloud, no telemetry, 100% offline processing.

---

## ✨ Features

- **📊 SEO Audit** — Analyze any URL for common SEO issues: missing title, meta description, H1 structure, images without `alt`, `robots.txt`, and `sitemap.xml` presence. Results are exported as a `.csv` report.
- **📝 Convert to Markdown** — Crawl an entire website and convert each HTML page into a clean Markdown file, stripped of scripts, styles, navbars, and footers. Ideal for RAG pipelines or documentation archiving.
- **🌐 Generate Sitemap & Robots.txt** — Recursively crawl a site to discover all internal URLs, generate a valid `sitemap.xml`, and save a local copy of the site's `robots.txt`.

---

## 🚀 Getting Started

### Option 1 — Download the prebuilt binary (no Python required)

Go to the [**Releases**](../../releases/latest) page and download the files for your platform:

#### 🪟 Windows

Download `WebSEOToolkit-windows.exe` and double-click it. That's it.

#### 🐧 Linux

Download both `WebSEOToolkit-linux.zip`, then run:

```bash
chmod +x install.sh
./install.sh
```

The installer will:
- Copy the binary to `~/.local/bin/`
- Create a `.desktop` entry so the app appears in your application menu
- Check for the `python3-tk` dependency and install it if missing

After that, launch **Web SEO Toolkit** directly from your application menu like any other app.

---

### Option 2 — Run from source (Python required)

#### Prerequisites

- Python **3.11+**
- A graphical environment (required for the Tkinter GUI)

> **Note for Linux Users (Ubuntu/Mint/Debian):** Modern Linux distributions implement PEP 668, which restricts system-wide `pip` installations. Use your native package manager or a virtual environment (see options below).

#### Installation

**Option A — Quick Install (System-wide via APT, Linux only)**

```bash
sudo apt update && sudo apt install python3-pandas python3-bs4 python3-requests python3-tk -y
```

**Option B — Clean Install (Virtual Environment, all platforms)**

1. Clone this repository or download the source files.
2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate       # Linux / macOS
venv\Scripts\activate          # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

> **⚠️ Windows-only packages:** `requirements.txt` includes `winrt-*`, `sounddevice`, and `vosk` which are Windows-specific or optional. On Linux/macOS, ignore pip errors for these packages — the core toolkit does not depend on them.

#### Running the Toolkit

```bash
python3 main.py
# or
./scripts/launch.sh      # Linux / macOS
scripts\launch.bat       # Windows
```

---

### Option 3 — Build the binary yourself

1. Clone this repository.
2. Run the build script (creates a venv automatically):

```bash
chmod +x scripts/build.sh
./scripts/build.sh
```

The standalone executable will be generated in the `dist/` folder.

---

## 📁 Project Structure

```
.
├── main.py              # Entry point — Tkinter GUI and action routing
├── seo_scanner.py       # SEO analysis logic (single page)
├── seo_crawler.py       # Recursive internal link crawler
├── page_scraper.py      # HTML-to-Markdown converter
├── sitemap_manager.py   # Sitemap XML generator and robots.txt fetcher
├── data_manager.py      # CSV export and log management
├── requirements.txt     # Python dependencies
└── scripts/
    ├── build.sh         # Build script (Linux / macOS)
    ├── launch.sh        # Launch from source (Linux / macOS)
    ├── launch.bat       # Launch from source (Windows)
    └── install.sh       # Installer for prebuilt binary (Linux)
```

Output files are saved under the `data/` directory by default (configurable via the GUI):

```
data/
├── csv/        # SEO audit reports
├── markdown/   # Converted Markdown pages
├── sitemaps/   # Generated sitemaps and robots.txt copies
└── logs/       # Execution logs
```

---

## 🛠️ Built With

| Library | Role |
|---|---|
| [Tkinter](https://docs.python.org/3/library/tkinter.html) | Native desktop GUI |
| [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) | HTML parsing and content extraction |
| [Requests](https://requests.readthedocs.io/) | Synchronous HTTP transactions |
| [Pandas](https://pandas.pydata.org/) | DataFrame compilation and CSV export |

---

## 🔒 Privacy & Safety

- **100% Local Processing** — No telemetry, no third-party APIs, no cloud storage. All crawls and scraped content stay on your machine.
- **User-Agent Header** — All HTTP requests identify as `MySEOBot/1.0`. Ensure you have authorization to crawl your target websites and that doing so complies with their `robots.txt` directives.