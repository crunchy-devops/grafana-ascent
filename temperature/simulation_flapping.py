import psycopg2
import time
from datetime import datetime

# Configuration PostgreSQL
DB_CONFIG = {
    "dbname": "grafana",
    "user": "user",
    "password": "password",
    "host": "postgres-db",
    "port": "5432"
}

def insert_temp(val):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO temperatures (time, value) VALUES (%s, %s)", (datetime.now(), val))
        conn.commit()
        cur.close()
        conn.close()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Température insérée : {val:.2f}°C")
    except Exception as e:
        print(f"Erreur : {e}")

def run_scenario():
    print("--- DEBUT DU SCENARIO ---")

    # 1. RAMP DOWN : +20°C à 0°C en 10 minutes (relevé toutes les 30s = 20 points)
    # Baisse de 1°C par palier
    temp = 10.0
    print("Phase 1 : Descente vers 0°C (10 min)...")
    for _ in range(10):
        insert_temp(temp)
        temp -= 1.0
        time.sleep(30)

        # 2. ALERTE : Passage sous 0°C pendant 5 minutes (pour tester le 'FOR 4m')
    # On reste à -5°C
    print("Phase 2 : Passage sous 0°C. L'alerte devrait passer en PENDING puis ALERTING après 4 min...")
    for _ in range(10):
        insert_temp(-5.0)
        time.sleep(30)

    # 3. REMONTÉE : On repasse au dessus de 0°C
    print("Phase 3 : Remontée à +5°C (Fin de l'alerte)...")
    for _ in range(4):
        insert_temp(5.0)
        time.sleep(30)

    # 4. FLAPPING : Oscillation entre -2°C et +2°C
    # Si l'anti-flapping est bien réglé, l'alerte ne doit pas se redéclencher
    print("Phase 4 : Flapping (-2°C / +2°C). L'alerte ne doit pas s'activer grâce au délai...")
    for _ in range(20):
        val = -2.0 if (_ % 2 == 0) else 2.0
        insert_temp(val)
        time.sleep(30)

if __name__ == "__main__":
    run_scenario()
