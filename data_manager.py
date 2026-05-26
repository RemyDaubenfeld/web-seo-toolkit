# region : IMPORTS
import os
from datetime import datetime
import pandas as pd
# endregion : IMPORTS

# region : DEFAULT FOLDER CONFIGURATION
LOG_OUTPUT_FOLDER = "data/logs"
CSV_OUTPUT_FOLDER = "data/csv"
# endregion : DEFAULT FOLDER CONFIGURATION

# region : FOLDER VERIFICATION
def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
# endregion : FOLDER VERIFICATION

# region : LOG RECORDING
def log_message(message):
    ensure_folder_exists(LOG_OUTPUT_FOLDER)
    date_str = datetime.now().strftime("%d-%m-%Y")
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    formatted = f"[{timestamp}] {message}"
    filename = f"execution_monitoring_{date_str}.log"
    log_path = os.path.join(LOG_OUTPUT_FOLDER, filename)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")
# endregion : LOG RECORDING

# region: AUDIT RESULTS EXPORT
def export_results(results_list, custom_folder=None):
    if not results_list:
        return None

    target_dir = custom_folder if custom_folder else CSV_OUTPUT_FOLDER
    ensure_folder_exists(target_dir)

    date_str = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"seo_audit_{date_str}.csv"
    file_path = os.path.join(target_dir, filename)

    df = pd.DataFrame(results_list)

    if 'errors' in df.columns:
        df['errors'] = df['errors'].apply(lambda x: " | ".join(x) if isinstance(x, list) else x)

    df.to_csv(file_path, index=False, encoding="utf-8-sig", sep=";")
    return file_path
# endregion: AUDIT RESULTS EXPORT