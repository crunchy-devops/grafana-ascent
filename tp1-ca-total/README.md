#  TP-1 Chiffres d'affaires (CA Total)
## introduction
Pour bien présenter le Chiffre d'Affaires (CA) total, 
l'objectif n'est pas seulement d'afficher un nombre, 
mais de donner du contexte (est-ce que c'est bien ? est-ce que ça monte ?).

Le meilleur choix dans Grafana est le **panel Stat**. 
Voici comment le configurer professionnellement :

## La Requete SQL
```sql92
SELECT 
  sum(p.price * oi.quantity) as value
FROM order_items oi
JOIN products p ON oi.product_id = p.id
JOIN orders o ON oi.order_id = o.id
WHERE o.status = 'completed' 
  AND $__timeFilter(o.order_date);
```
## Configuration du Panel "Stat" (Le visuel)
Dans la barre latérale droite de Grafana, 
appliquez les réglages suivants pour transformer 
un simple chiffre en indicateur pro :

### Standard Options (Unité et Précision)
- Unit : Choisissez Currency > Euro (€) (ou votre devise). Cela ajoute automatiquement
le symbole et sépare les milliers.

- Decimals : Réglez sur 2 pour éviter les arrondis imprécis sur les centimes.
### Stat Styles (Mise en page)
- Graph mode : Choisissez Area graph. Cela affichera une petite courbe colorée sous le chiffre, montrant l'évolution sur la période. C'est très visuel pour voir les pics de vente.

- Color mode : Choisissez Background ou Value.

- Text mode : Value and Name (pour afficher le titre "CA Total" clairement).

### Thresholds (Seuils de performance)
C'est ici que vous donnez du sens au chiffre. 
Si le CA est faible, il s'affiche en rouge ; s'il est bon, en vert.

- Base : Rouge.

- Seuil 1 (ex: 5000) : Orange.

- Seuil 2 (ex: 10000) : Vert.

### Ajouter une "Valeur de comparaison"
Pour un dashboard métier, il est utile de savoir si le CA actuel 
est supérieur ou inférieur à celui de la veille.

1- Allez dans l'onglet Transform du panel.

2- Utilisez Add field from calculation.

3- Calculez la différence ou le pourcentage de variation. 
Alternativement : Utilisez l'option "Calculation" dans le panel Stat 
réglée sur "Difference" si vous avez deux séries de données.

### Resume des bonnes pratiques

| À faire  |  Pourquoi ?   |   
|---|---|---|---|---|
| Utiliser le filtre $__timeFilter   | Évite de faire planter le navigateur en limitant les données.   |   
| Ajouter un Sparkline (Area graph) | Permet de voir la tendance sans créer un deuxième graphique.  |   
| Définir des Thresholds  | Permet une lecture immédiate de la santé du business. |   
