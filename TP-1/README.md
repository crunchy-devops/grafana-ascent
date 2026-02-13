le **suivi des transactions** (commits et rollbacks),  c'est un excellent indicateur pour détecter si une application rencontre des erreurs massives.

# ---

**TP : Monitoring PostgreSQL Avancé (20 min)**

**Objectif :** Créer un dashboard de santé PostgreSQL et configurer une alerte intelligente contre le "flapping".

## ---

**1\. Analyse des Transactions (Panel Stat \- 7 min)**
nous allons surveiller le nombre de **Commits** (succès) par base de données pour voir l'activité réelle.

1. **Créer une Variable** : Allez dans *Dashboard Settings \> Variables*. Nommez-la dbname, type Query.  
   * Requête : SELECT datname FROM pg\_database WHERE datname NOT LIKE 'template%';  
2. **Créer le Panel Stat** :  
   * **SQL** :  
     SQL  
     SELECT   
       now() as time,  
       datname as "db\_name",  
       xact\_commit as "commits"  
     FROM pg\_stat\_database  
     WHERE datname IN ($dbname);

   * **Format as** : Table.  
   * **Transformations** :  
     1. *Partition by values* sur le champ db\_name.  
     2. *Prepare time series* (Multi-frame).  
   * **Style** : Dans *Standard Options \> Display Name*, utilisez ${\_\_series.name}.  
   * **Sparkline** : Activez le mode *Area*. Cela permet de voir si l'activité d'une DB chute brutalement.

## ---

**2\. Taux de Succès du Cache (Panel Gauge \- 5 min)**

Le "Cache Hit Ratio" indique si PostgreSQL trouve les données en mémoire vive (rapide) ou sur le disque (lent).

1. **Ajouter un Panel Gauge** :  
   * **SQL** :  
     SQL  
     SELECT   
       sum(blks\_hit) / (sum(blks\_hit) \+ sum(blks\_read) \+ 1) \* 100   
     FROM pg\_stat\_database;

   * **Configuration** :  
     * *Min* : 0, *Max* : 100, *Unit* : Percent (%).  
     * *Thresholds* : 0 (Rouge), 90 (Jaune), 95 (Vert).  
2. **Objectif** : Si la jauge descend sous 90%, il faut probablement augmenter la RAM (shared\_buffers).

## ---

**3\. Alerte Anti-Flapping sur les Rollbacks (8 min)**

Un "Rollback" signifie qu'une transaction a échoué. On veut être alerté si cela arrive trop souvent.

1. **Créer l'Alerte** :  
   * Sur un panneau surveillant xact\_rollback, créez une règle.  
   * **Condition** : IS ABOVE 10 (erreurs par minute).  
2. **Configuration du "For" (Anti-flapping)** :  
   * Réglez le champ **Pending period (For)** sur 4m.  
   * **Validation** : L'étudiant doit expliquer que si une erreur réseau passagère de 30 secondes survient, l'alerte passera en "Pending" mais n'enverra pas d'email inutilement.

## ---

**4\. Correction du temps (UTC vs Local)**

* **Exercice** : Si les commits semblent enregistrés dans le futur ou le passé, forcez le Dashboard en Browser Time.  
* **Vérification** : Regardez dans le *Query Inspector* si le temps envoyé par PostgreSQL correspond à la fenêtre de temps de Grafana.

### ---

**Pourquoi ce choix ?**

Les **transactions** et le **cache hit ratio** sont les indicateurs que les administrateurs de bases de données (DBA) surveillent quotidiennement.

