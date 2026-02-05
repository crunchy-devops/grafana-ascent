# Indicateur
Pour ajouter un deuxième indicateur (comme le nombre de commandes) dans le même espace visuel, il existe deux approches 
utiliser le mode "All Values" du panel Stat ou utiliser des séries multiples.

## La Requête SQL (Deux colonnes)
Cette requete renvoie deux mesures distinctes : le montant total et le compte unique des commandes.

```sql92
SELECT 
  sum(p.price * oi.quantity) as "Chiffre d'Affaires",
  count(DISTINCT o.id) as "Nombre de Commandes"
FROM order_items oi
JOIN products p ON oi.product_id = p.id
JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed' 
  AND $__timeFilter(o.order_date);
```

Configuration pour l'affichage vertical
Par défaut, Grafana peut essayer de mettre les deux chiffres côte à côte. Pour les empiler :

1. Orientation : Dans les réglages du panel (à droite), cherchez l'option Orientation et forcez-la sur Vertical. 
Cela placera le CA au-dessus du nombre de commandes.

2. Text size : Vous pouvez ajuster la taille du titre (Title size) et de la valeur (Value size) pour que le CA soit 
plus gros que l'indicateur secondaire.

## Gérer les unités différentes (Overrides)
C'est l'étape cruciale : le CA doit être en Euros, mais le nombre de commandes ne 
doit pas avoir d'unité. Pour cela, on utilise les Overrides.

1. Allez dans l'onglet Overrides (juste à côté de "Settings" à droite).

2. Cliquez sur + Add field override > Fields with name.

3. Sélectionnez Chiffre d'Affaires.

4. Ajoutez une propriété (Add property) : Standard options > Unit et réglez sur Euro (€).

5. Faites de même pour Nombre de Commandes mais choisissez l'unité Short (ou aucune) 
pour rester sur un nombre entier.