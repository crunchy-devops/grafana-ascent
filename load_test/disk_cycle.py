import os
import time
import subprocess
from datetime import datetime
from threading import Thread

# Configuration
TARGET_DIR = "./disk_test"
FILE_PREFIX = "test_file_"
CREATE_INTERVAL = 1800 # 30 minutes
DELETE_INTERVAL = 5400  # 1 heure 30

if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)

def create_file():
    while True:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(TARGET_DIR, f"{FILE_PREFIX}{timestamp}.bin")
        print(f"[{datetime.now()}] Création de {filename}...")

        # Commande dd : 1G de zéros
        subprocess.run(["dd", "if=/dev/zero", f"of={filename}", "bs=2G", "count=1"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        time.sleep(CREATE_INTERVAL)

def delete_oldest():
    while True:
        time.sleep(DELETE_INTERVAL)
        files = [os.path.join(TARGET_DIR, f) for f in os.listdir(TARGET_DIR) if f.startswith(FILE_PREFIX)]
        if files:
            # On trie par date de création
            files.sort(key=os.path.getmtime)
            oldest_file = files[0]
            print(f"[{datetime.now()}] Suppression de {oldest_file}")
            os.remove(oldest_file)
        else:
            print(f"[{datetime.now()}] Aucun fichier à supprimer.")

if __name__ == "__main__":
    print("Démarrage du cycle disque...")
    Thread(target=create_file).start()
    Thread(target=delete_oldest).start()
