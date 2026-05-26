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

# region : INTERFACE DE SUIVI (CONSOLE)
def create_status_window(title_text="Traitement en cours"):
    global status_window, status_area, progress_bar, counter_label

    status_window = Tk()
    status_window.title(title_text)
    status_window.geometry("650x500")
    status_window.resizable(False, False)

    counter_label = Label(status_window, text="Initialisation...", font=("Helvetica", 10, "italic"))
    counter_label.pack(side=BOTTOM, fill=X, padx=20, pady=5)

    progress_bar = ttk.Progressbar(status_window, orient=HORIZONTAL, length=400, mode='determinate')
    progress_bar.pack(side=BOTTOM, fill=X, padx=20, pady=5)

    status_area = Text(status_window, bg="black", fg="white", font=("Consolas", 10), padx=10, pady=10)
    status_area.pack(side=TOP, fill="both", expand=True, padx=5, pady=5)
    status_area.insert(END, "--- Début de l'opération ---\n")
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
       print(f"Erreur update_status: {e}") 

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
        prefix = "\n\n🛑 ERREUR CRITIQUE : "
        color = "#ff4444"
        btn_text = "Quitter le programme"
        system_command = sys.exit
    else:
        prefix = "\n\n✅ OPÉRATION TERMINÉE : "
        color = "#44ff44"
        btn_text = "Fermer la fenêtre"
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
# endregion : INTERFACE DE SUIVI (CONSOLE)

# region : VERIFICATIONS SYSTEME
def check_scripts():
    SCRIPTS = ["seo_scanner.py", "data_manager.py", "seo_crawler.py", "page_scraper.py", "sitemap_manager.py"]
    FILES = ["requirements.txt"]
    missing_files = [f for f in SCRIPTS + FILES if not os.path.exists(f)]
    
    if missing_files:
        messagebox.showerror("Erreur", f"Fichiers manquants : {', '.join(missing_files)}")
        sys.exit()

def check_deps():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
    except Exception as e:
        print("\n💡 [Note] L'environnement système bloque pip (PEP 668).")
        print("Si des modules manquent, exécutez : sudo apt install python3-pandas python3-bs4 python3-requests")
# endregion : VERIFICATIONS SYSTEME

# region : GESTION DES ACTIONS ET PARCOURS
def browse_output_folder():
    global target_folder
    selected_dir = filedialog.askdirectory(title="Choisir le dossier d'enregistrement")
    if selected_dir:
        target_folder = os.path.abspath(selected_dir)
        folder_entry.config(state=NORMAL)
        folder_entry.delete(0, END)
        folder_entry.insert(0, target_folder)
        folder_entry.config(state=DISABLED)

def run_seo_audit():
    url = url_entry.get().strip()
    if not url or url == "https://":
        messagebox.showwarning("Attention", "Veuillez entrer une URL valide.")
        return
    
    output_dir = target_folder if target_folder else "data/csv"
    
    create_status_window("Audit SEO en cours")
    update_status(f"🚀 Initialisation de l'audit SEO pour : {url}")
    
    import seo_scanner
    import data_manager
    
    progress_bar["maximum"] = 1
    progress_bar["value"] = 0
    counter_label.config(text="Analyse de la page racine...", fg="blue")
    
    data = seo_scanner.run_analysis(url)
    
    if not data or "error" in data:
        finish_session("L'analyse a échoué.", is_error=True)
        return
        
    progress_bar["value"] = 1
    errors_list = data.get("errors", [])
    update_status(f"📊 {len(errors_list)} problème(s) détecté(s).")
    
    filename = data_manager.export_results([data], custom_folder=output_dir)
    update_status(f"\n📂 Rapport exporté avec succès dans : ", export_path=filename)
    
    counter_label.config(text="Analyse terminée", fg="green")
    finish_session(f"Rapport sauvegardé avec succès.", is_error=False)

def run_markdown_extractor():
    url = url_entry.get().strip()
    if not url or url == "https://":
        messagebox.showwarning("Attention", "Veuillez entrer une URL valide.")
        return
        
    output_dir = target_folder if target_folder else "data/markdown"
    
    create_status_window("Conversion du site en Markdown")
    
    from seo_crawler import SEOCrawler
    import page_scraper
    import data_manager
    
    def console_write(msg):
        update_status(msg)
        
    def progress_update(current, total):
        progress_bar["maximum"] = total
        progress_bar["value"] = current
        counter_label.config(text=f"Extraction : {current} / {total}", fg="blue")
        status_window.update_idletasks()

    update_status(f"🕵️ Étape 1 : Cartographie des liens pour : {url}\n")
    crawler = SEOCrawler(url)
    urls_to_scrape = crawler.get_url_list(update_callback=console_write)
    
    total_urls = len(urls_to_scrape)
    if total_urls == 0:
        finish_session("Aucune URL interne découverte.", is_error=True)
        return
        
    update_status(f"\n✅ {total_urls} page(s) détectée(s). Début de la conversion Markdown...\n")
    
    domain_name = urlparse(url).netloc.replace('.', '_')
    final_output_path = os.path.join(output_dir, domain_name)
    
    success, errors = page_scraper.scrape_multiple_urls(
        urls=urls_to_scrape,
        output_folder=final_output_path,
        status_callback=console_write,
        progress_callback=progress_update
    )
    
    counter_label.config(text="Conversion terminée !", fg="green")
    finish_session(f"Extraction terminée. Succès : {success} | Échecs : {errors}\nFichiers stockés dans : {final_output_path}", is_error=False)

def run_sitemap_generator():
    url = url_entry.get().strip()
    if not url or url == "https://":
        messagebox.showwarning("Attention", "Veuillez entrer une URL valide.")
        return
        
    output_dir = target_folder if target_folder else "data/sitemaps"
    
    create_status_window("Génération du Sitemap & Extraction Robots.txt")
    update_status(f"🚀 Démarrage de l'exploration de structure pour : {url}\n")
    
    from seo_crawler import SEOCrawler
    import sitemap_manager
    
    # 1. Extraction du fichier Robots.txt externe
    update_status("🤖 Récupération du fichier robots.txt...")
    robots_data = sitemap_manager.download_robots_txt(url)
    
    # 2. Cartographie du site
    update_status("\n🕸️ Scan des liens internes...")
    crawler = SEOCrawler(url)
    urls = crawler.get_url_list(update_callback=lambda msg: update_status(msg))
    
    # 3. Structuration du dossier de sauvegarde
    domain_name = urlparse(url).netloc.replace('.', '_')
    dossier_final = os.path.join(output_dir, domain_name)
    os.makedirs(dossier_final, exist_ok=True)
    
    # 4. Enregistrement Sitemap XML
    sitemap_path = os.path.join(dossier_final, "sitemap.xml")
    sitemap_manager.generate_xml_sitemap(urls, sitemap_path)
    update_status(f"\n🗺️ Sitemap XML créé : ", export_path=sitemap_path)
    
    # 5. Enregistrement Robots.txt local
    robots_path = os.path.join(dossier_final, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_data)
    update_status(f"🤖 Copie de Robots.txt créée : ", export_path=robots_path)
    
    counter_label.config(text="Sitemap & Robots créés !", fg="green")
    finish_session(f"Génération terminée avec succès.\nFichiers stockés dans : {dossier_final}", is_error=False)
# endregion : GESTION DES ACTIONS ET PARCOURS

# region : FENETRE PRINCIPALE (MENU CONFIGURATION)
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
    Label(frame_url, text="Target URL :", font=("Helvetica", 10, "bold")).pack(anchor=W)
    url_entry = Entry(frame_url, font=("Consolas", 11), width=50)
    url_entry.insert(0, "https://")
    url_entry.pack(fill=X, pady=5)
    
    # Frame Destination Dossier
    frame_folder = Frame(root, padx=15, pady=5)
    frame_folder.pack(fill=X)
    Label(frame_folder, text="Output Folder (Optional) :", font=("Helvetica", 10, "bold")).pack(anchor=W)
    
    frame_sub_folder = Frame(frame_folder)
    frame_sub_folder.pack(fill=X, pady=5)
    
    folder_entry = Entry(frame_sub_folder, font=("Consolas", 10), state=DISABLED)
    folder_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
    
    btn_browse = Button(frame_sub_folder, text="Browse...", command=browse_output_folder)
    btn_browse.pack(side=RIGHT)
    
    # Frame Boutons Actions
    frame_actions = Frame(root, pady=15)
    frame_actions.pack()
    
    btn_seo = Button(frame_actions, text="📊 Run SEO Audit", font=("Helvetica", 10, "bold"), bg="#4caf50", fg="white", width=25, command=run_seo_audit)
    btn_seo.grid(row=0, column=0, padx=10, pady=5)
    
    btn_md = Button(frame_actions, text="📝 Convert to Markdown", font=("Helvetica", 10, "bold"), bg="#2196f3", fg="white", width=25, command=run_markdown_extractor)
    btn_md.grid(row=0, column=1, padx=10, pady=5)
    
    btn_sitemap = Button(frame_actions, text="🌐 Generate Sitemap & Robots.txt", font=("Helvetica", 10, "bold"), bg="#9c27b0", fg="white", width=54, command=run_sitemap_generator)
    btn_sitemap.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    
    root.mainloop()
# endregion : FENETRE PRINCIPALE (MENU CONFIGURATION)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    check_scripts()
    check_deps()       
    import data_manager 
    main_menu()