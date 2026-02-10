CREATE TABLE temperatures (
                              id SERIAL PRIMARY KEY,
                              value DECIMAL(4, 2), -- Permet des valeurs comme -15.50
                              time TIMESTAMPTZ DEFAULT now()
);
