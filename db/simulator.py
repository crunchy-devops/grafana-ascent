import psycopg2
import random
import time
from datetime import datetime

# CONFIGURATION - À adapter selon vos identifiants AlmaLinux
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "ma_base_donnees",
    "user": "admin_user",
    "password": "password_db"
}

def run_simulation():
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("🚀 Simulateur de ventes activé...")

        # Récupérer les IDs de produits existants
        cur.execute("SELECT id FROM products")
        product_ids = [row[0] for row in cur.fetchall()]

        if not product_ids:
            print("❌ Erreur : La table 'products' est vide. Exécutez le script SQL d'abord.")
            return

        while True:
            # 1. Générer une commande
            status = random.choices(
                ['completed', 'pending', 'canceled'],
                weights=[70, 20, 10] # 70% de succès pour les graphiques
            )[0]

            cur.execute(
                "INSERT INTO orders (customer_id, order_date, status) VALUES (%s, %s, %s) RETURNING id",
                (random.randint(1000, 9999), datetime.now(), status)
            )
            order_id = cur.fetchone()[0]

            # 2. Ajouter entre 1 et 4 produits à cette commande
            nb_articles = random.randint(1, 4)
            for _ in range(nb_articles):
                p_id = random.choice(product_ids)
                qty = random.randint(1, 5)

                cur.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (order_id, p_id, qty)
                )

            conn.commit()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Commande #{order_id} créée : {nb_articles} articles (Statut: {status})")

            # Pause aléatoire entre 2 et 8 secondes pour simuler un trafic réel
            time.sleep(random.uniform(2, 8))

    except KeyboardInterrupt:
        print("\n🛑 Simulation arrêtée par l'utilisateur.")
    except Exception as e:
        print(f"❌ Erreur système : {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    run_simulation()