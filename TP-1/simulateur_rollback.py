import psycopg2
import time
import random
from datetime import datetime

# Configuration de la connexion
DB_CONFIG = {
    "dbname": "monitoring_db",
    "user": "grafana_user",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def simulate_activity():
    print("🚀 Démarrage de la simulation d'activité...")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False # Important pour pouvoir faire des rollbacks manuels
        cur = conn.cursor()

        while True:
            now = datetime.now().strftime("%H:%M:%S")
            # Probabilité de panne (30% de chances de générer des erreurs massives)
            fail_mode = random.random() < 0.3

            if fail_mode:
                print(f"[{now}] ⚠️ MODE ERREUR : Génération de 50 rollbacks...")
                for _ in range(50):
                    try:
                        # On tente une insertion invalide (ex: division par zéro ou table inexistante)
                        cur.execute("SELECT 1/0;")
                        conn.commit()
                    except:
                        conn.rollback() # Cela incrémente xact_rollback dans pg_stat_database
                time.sleep(5) # On laisse l'erreur persister pour le "For 4m"
            else:
                print(f"[{now}] ✅ MODE NORMAL : 10 transactions réussies.")
                for _ in range(10):
                    cur.execute("SELECT 1;")
                    conn.commit()
                time.sleep(10)

    except Exception as e:
        print(f"Erreur de connexion : {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    simulate_activity()