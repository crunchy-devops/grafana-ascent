-- Nettoyage si besoin (Attention : supprime les données existantes)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;

-- 1. Table des produits (Le catalogue)
CREATE TABLE products (
                          id SERIAL PRIMARY KEY,
                          name VARCHAR(100),
                          category VARCHAR(50),
                          price DECIMAL(10, 2)
);

-- 2. Table des commandes (Le flux temporel)
CREATE TABLE orders (
                        id SERIAL PRIMARY KEY,
                        customer_id INT,
                        order_date TIMESTAMPTZ DEFAULT now(),
                        status VARCHAR(20) -- 'completed', 'pending', 'canceled'
);

-- 3. Table de détails (Le lien pour le calcul CA)
CREATE TABLE order_items (
                             id SERIAL PRIMARY KEY,
                             order_id INT REFERENCES orders(id) ON DELETE CASCADE,
                             product_id INT REFERENCES products(id),
                             quantity INT NOT NULL
);

-- Insertion du catalogue de base
INSERT INTO products (name, category, price) VALUES
                     ('Station de travail Pro', 'Tech', 3500.00),
                     ('Écran 4K 32"', 'Tech', 650.00),
                     ('Clavier Ergonomique', 'Tech', 120.00),
                     ('Abonnement Cloud Annuel', 'Service', 1200.00),
                     ('Support Technique Premium', 'Service', 500.00),
                     ('Café de Spécialité 1kg', 'Food', 35.00);