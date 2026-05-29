# region : IMPORTS
import sys
import os
import subprocess
from datetime import datetime
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from urllib.parse import urlparse
# endregion : IMPORTS

# region : GLOBALS & CONFIG
status_window = None
status_area = None
btn_quit = None
url_entry = None
folder_entry = None
target_folder = ""
# endregion : GLOBALS & CONFIG

# region : STATUS WINDOW (CONSOLE)
def create_status_window(title_text="Processing..."):
    global status_window, status_area, progress_bar, counter_label

    status_window = Tk()
    status_window.title(title_text)
    status_window.geometry("650x500")
    status_window.resizable(False, False)

    counter_label = Label(status_window, text="Initializing...", font=("Helvetica", 10, "italic"))
    counter_label.pack(side=BOTTOM, fill=X, padx=20, pady=5)

    progress_bar = ttk.Progressbar(status_window, orient=HORIZONTAL, length=400, mode='determinate')
    progress_bar.pack(side=BOTTOM, fill=X, padx=20, pady=5)

    status_area = Text(status_window, bg="black", fg="white", font=("Consolas", 10), padx=10, pady=10)
    status_area.pack(side=TOP, fill="both", expand=True, padx=5, pady=5)
    status_area.insert(END, "--- Operation started ---\n")
    status_window.update()

def update_status(message, export_path=None):
    global status_area, status_window
    try:
        if export_path:
            status_area.insert(END, message)
            status_area.insert(END, export_path, "link")
            status_area.insert(END, "\n")
            status_area.tag_config("link", foreground="cyan", underline=1)
            status_area.tag_bind("link", "<Button-1>", lambda e: open_file(path=export_path))
            status_area.tag_bind("link", "<Enter>", lambda e: status_area.config(cursor="hand2"))
            status_area.tag_bind("link", "<Leave>", lambda e: status_area.config(cursor=""))
        else:
            status_area.insert(END, f"{message}\n")

        status_area.see(END)
        status_window.update()
    except Exception as e:
        print(f"update_status error: {e}")

def open_file(event=None, path=None):
    abs_path = os.path.abspath(path)
    if os.path.exists(abs_path):
        if sys.platform == "win32":
            os.startfile(abs_path)
        else:
            subprocess.run(["open", abs_path])

def finish_session(message, is_error=False):
    global status_area, btn_quit, status_window

    if is_error:
        prefix = "\n\n🛑 CRITICAL ERROR: "
        color = "#ff4444"
        btn_text = "Quit"
        system_command = sys.exit
    else:
        prefix = "\n\n✅ OPERATION COMPLETE: "
        color = "#44ff44"
        btn_text = "Close"
        system_command = status_window.destroy

    update_status(f"{prefix}{message}")

    btn_quit = Button(status_window, text=btn_text, bg=color, font=("Helvetica", 10, "bold"), command=system_command)

    status_area.pack_forget()
    counter_label.pack_forget()
    progress_bar.pack_forget()

    btn_quit.pack(side=BOTTOM, pady=10)
    status_area.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
    counter_label.pack(side=BOTTOM, fill=X, padx=20, pady=5)

    status_window.update()
    status_window.mainloop()
# endregion : STATUS WINDOW (CONSOLE)

# region : SYSTEM CHECKS
def is_frozen():
    """Returns True if running inside a PyInstaller bundle."""
    return getattr(sys, 'frozen', False)

def check_scripts():
    if is_frozen():
        return

    SCRIPTS = ["seo_scanner.py", "data_manager.py", "seo_crawler.py", "page_scraper.py", "sitemap_manager.py"]
    FILES = ["requirements.txt"]
    missing_files = [f for f in SCRIPTS + FILES if not os.path.exists(f)]

    if missing_files:
        messagebox.showerror("Error", f"Missing files: {', '.join(missing_files)}")
        sys.exit()

def check_deps():
    if is_frozen():
        return

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
    except Exception as e:
        print("\n💡 [Note] System environment blocks pip (PEP 668).")
        print("If modules are missing, run: sudo apt install python3-pandas python3-bs4 python3-requests")
# endregion : SYSTEM CHECKS

# region : ACTION HANDLERS
def browse_output_folder():
    global target_folder
    selected_dir = filedialog.askdirectory(title="Select output folder")
    if selected_dir:
        target_folder = os.path.abspath(selected_dir)
        folder_entry.config(state=NORMAL)
        folder_entry.delete(0, END)
        folder_entry.insert(0, target_folder)
        folder_entry.config(state=DISABLED)

def run_seo_audit():
    url = url_entry.get().strip()
    if not url or url == "https://":
        messagebox.showwarning("Warning", "Please enter a valid URL.")
        return

    output_dir = target_folder if target_folder else "data/csv"

    create_status_window("SEO Audit in progress")
    update_status(f"🚀 Starting SEO audit for: {url}")

    import seo_scanner
    import data_manager

    progress_bar["maximum"] = 1
    progress_bar["value"] = 0
    counter_label.config(text="Analyzing root page...", fg="blue")

    data = seo_scanner.run_analysis(url)

    if not data or "error" in data:
        finish_session("Analysis failed.", is_error=True)
        return

    progress_bar["value"] = 1
    errors_list = data.get("errors", [])
    update_status(f"📊 {len(errors_list)} issue(s) detected.")

    filename = data_manager.export_results([data], custom_folder=output_dir)
    update_status(f"\n📂 Report successfully exported to: ", export_path=filename)

    counter_label.config(text="Analysis complete", fg="green")
    finish_session("Report saved successfully.", is_error=False)

def run_sitemap_generator():
    url = url_entry.get().strip()
    if not url or url == "https://":
        messagebox.showwarning("Warning", "Please enter a valid URL.")
        return

    output_dir = target_folder if target_folder else "data/sitemaps"

    create_status_window("Sitemap & Robots.txt Generation")
    update_status(f"🚀 Starting site structure crawl for: {url}\n")

    from seo_crawler import SEOCrawler
    import sitemap_manager

    update_status("🤖 Fetching robots.txt...")
    robots_data = sitemap_manager.download_robots_txt(url)

    update_status("\n🕸️ Scanning internal links...")
    crawler = SEOCrawler(url)
    urls = crawler.get_url_list(update_callback=lambda msg: update_status(msg))

    domain_name = urlparse(url).netloc.replace('.', '_')
    dossier_final = os.path.join(output_dir, domain_name)
    os.makedirs(dossier_final, exist_ok=True)

    sitemap_path = os.path.join(dossier_final, "sitemap.xml")
    sitemap_manager.generate_xml_sitemap(urls, sitemap_path)
    update_status(f"\n🗺️ Sitemap XML created: ", export_path=sitemap_path)

    robots_path = os.path.join(dossier_final, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_data)
    update_status(f"🤖 Robots.txt copy saved: ", export_path=robots_path)

    counter_label.config(text="Sitemap & Robots.txt created!", fg="green")
    finish_session(f"Generation complete.\nFiles saved to: {dossier_final}", is_error=False)

def run_markdown_extractor():
    url = url_entry.get().strip()
    if not url or url == "https://":
        messagebox.showwarning("Warning", "Please enter a valid URL.")
        return

    output_dir = target_folder if target_folder else "data/markdown"

    create_status_window("Converting website to Markdown")

    from seo_crawler import SEOCrawler
    import page_scraper
    import data_manager

    def console_write(msg):
        update_status(msg)

    def progress_update(current, total):
        progress_bar["maximum"] = total
        progress_bar["value"] = current
        counter_label.config(text=f"Extracting: {current} / {total}", fg="blue")
        status_window.update_idletasks()

    update_status(f"🕵️ Step 1: Mapping links for: {url}\n")
    crawler = SEOCrawler(url)
    urls_to_scrape = crawler.get_url_list(update_callback=console_write)

    total_urls = len(urls_to_scrape)
    if total_urls == 0:
        finish_session("No internal URLs discovered.", is_error=True)
        return

    update_status(f"\n✅ {total_urls} page(s) found. Starting Markdown conversion...\n")

    domain_name = urlparse(url).netloc.replace('.', '_')
    final_output_path = os.path.join(output_dir, domain_name)

    success, errors = page_scraper.scrape_multiple_urls(
        urls=urls_to_scrape,
        output_folder=final_output_path,
        status_callback=console_write,
        progress_callback=progress_update
    )

    counter_label.config(text="Conversion complete!", fg="green")
    finish_session(f"Extraction complete. Success: {success} | Failures: {errors}\nFiles saved to: {final_output_path}", is_error=False)

def run_single_page_scraper():
    url = url_entry.get().strip()
    if not url or url == "https://":
        messagebox.showwarning("Warning", "Please enter a valid URL.")
        return

    output_dir = target_folder if target_folder else "data/markdown"

    create_status_window("Converting page to Markdown")
    update_status(f"🔍 Converting page : {url}\n")
 
    import page_scraper
 
    progress_bar["maximum"] = 1
    progress_bar["value"] = 0
    counter_label.config(text="Conversion in progress...", fg="blue")
 
    try:
        filepath = page_scraper.scrape_page(url, output_folder=output_dir)
        progress_bar["value"] = 1
        update_status(f"\n📄 Markdown file created : ", export_path=filepath)
        counter_label.config(text="Conversion complete !", fg="green")
        finish_session(f"Page successfully converted.", is_error=False)
    except Exception as e:
        finish_session(f"Conversion failed : {str(e)}", is_error=True)
# endregion : ACTION HANDLERS

# region : MAIN MENU
def main_menu():
    global url_entry, folder_entry

    root = Tk()
    root.title("Web Scraper & SEO Audit - Config")
    root.geometry("600x380")
    root.resizable(False, False)

    Label(root, text="Scan Settings", font=("Helvetica", 14, "bold"), pady=10).pack()

    # Frame URL
    frame_url = Frame(root, padx=15, pady=5)
    frame_url.pack(fill=X)
    Label(frame_url, text="Target URL:", font=("Helvetica", 10, "bold")).pack(anchor=W)
    url_entry = Entry(frame_url, font=("Consolas", 11), width=50)
    url_entry.insert(0, "https://")
    url_entry.pack(fill=X, pady=5)

    # Frame folder
    frame_folder = Frame(root, padx=15, pady=5)
    frame_folder.pack(fill=X)
    Label(frame_folder, text="Output Folder (Optional):", font=("Helvetica", 10, "bold")).pack(anchor=W)

    frame_sub_folder = Frame(frame_folder)
    frame_sub_folder.pack(fill=X, pady=5)

    folder_entry = Entry(frame_sub_folder, font=("Consolas", 10), state=DISABLED)
    folder_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

    btn_browse = Button(frame_sub_folder, text="Browse...", command=browse_output_folder)
    btn_browse.pack(side=RIGHT)
    
    # Frame action button
    frame_actions = Frame(root, pady=15)
    frame_actions.pack()


    # Colonne SEO
    frame_seo = Frame(frame_actions, padx=10)
    frame_seo.grid(row=0, column=0, sticky=N)
 
    Label(frame_seo, text="🔎 SEO", font=("Helvetica", 10, "bold")).pack(pady=(0, 5))
 
    btn_seo = Button(frame_seo, text="📊 Run SEO Audit", font=("Helvetica", 10, "bold"), bg="#4caf50", fg="white", width=25, command=run_seo_audit)
    btn_seo.pack(pady=5)
 
    btn_sitemap = Button(frame_seo, text="🌐 Generate Sitemap & Robots.txt", font=("Helvetica", 10, "bold"), bg="#9c27b0", fg="white", width=25, command=run_sitemap_generator)
    btn_sitemap.pack(pady=5)
 
    # Séparateur vertical
    Frame(frame_actions, width=2, bg="#cccccc").grid(row=0, column=1, sticky=NS, padx=5, pady=5)
 
    # Colonne Scraping
    frame_scraping = Frame(frame_actions, padx=10)
    frame_scraping.grid(row=0, column=2, sticky=N)
 
    Label(frame_scraping, text="🕷️ Scraping (convert to Markdown)", font=("Helvetica", 10, "bold")).pack(pady=(0, 5))
 
    btn_single = Button(frame_scraping, text="🔍 Scrape Single Page", font=("Helvetica", 10, "bold"), bg="#ff9800", fg="white", width=25, command=run_single_page_scraper)
    btn_single.pack(pady=5)
 
    btn_md = Button(frame_scraping, text="📝 Scrape All Site", font=("Helvetica", 10, "bold"), bg="#2196f3", fg="white", width=25, command=run_markdown_extractor)
    btn_md.pack(pady=5)

    root.mainloop()
# endregion : MAIN MENU

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    check_scripts()
    check_deps()
    import data_manager
    main_menu()