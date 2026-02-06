# Temperature 
Voici la démarche complète pour intégrer la gestion de la température,
du stockage à l'alerte anti-flapping.

## Structure SQL (Table Température)
Exécutez ce script pour créer la table. L'utilisation de TIMESTAMPTZ est 
recommandée pour éviter les décalages horaires dans Grafana.
```sql
CREATE TABLE temperatures (
             id SERIAL PRIMARY KEY,
             value DECIMAL(4, 2), -- Permet des valeurs comme -15.50
             time TIMESTAMPTZ DEFAULT now()
);
```
## Mise à jour du simulateur (simulator.py)
Ajoutez cette fonction à votre script Python pour insérer une donnée 
toutes les 5 minutes (ou moins pour vos tests).

## Configuration du Panel Gauge (Le visuel)
```sql
SELECT 
  time, 
  value 
FROM temperatures 
WHERE $__timeFilter(time) 
ORDER BY time DESC 
LIMIT 1; -- On ne veut que la valeur la plus récente
```

### Réglages du Panel Gauge :
1. Unit : Celsius (°C).
2. Min : -20 / Max : 40.
3. Thresholds (Seuils) :
 * Base : Blue (Froid)
 * 0 : Light Blue
 * 20 : Orange
 * 30 : Red (Chaud)

## Alerte Temperature Negative (20 min)
1. Dans le panel, onglet Alert, créez une règle.
2. Condition : WHEN last() OF query(A) IS BELOW 0.
3. Délai (For) : Réglez sur 20m.
  * Explication : Grafana attendra que la température reste sous zéro pendant 20 minutes
    consécutives avant de déclencher l'alerte.

## Qu'est ce l'anti-flapping ?
L'anti-flapping est un mécanisme essentiel en monitoring qui permet de filtrer le « bruit » 
généré par une métrique instable.
Imaginez une température qui oscille entre -0.1°C et +0.1°C toutes les 30 secondes alors que votre seuil d'alerte est à 0°C. 
Sans anti-flapping, vous recevriez des dizaines de notifications Slack « Alerte » suivies de « OK » (c'est ce qu'on appelle le flapping).
