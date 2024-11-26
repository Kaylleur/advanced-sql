
# GROUPING SETS, ROLLUP, et CUBE en SQL

## Contexte :
Nous allons travailler avec les tables suivantes :
- **orders** : contient les commandes avec `id`, `customer_id`, et `order_date`.
- **order_items** : contient les articles des commandes avec `id`, `order_id`, `product_id`, `quantity`, et `price`.

### Objectif :
Calculer les totaux des ventes (somme des prix) par différentes dimensions comme `order_date`, `customer_id`, et `product_id`.

---

## 1. GROUPING SETS

### Description :
- Permet de spécifier des groupes précis pour lesquels on veut des agrégats.
- Flexible : idéal pour calculer des totaux partiels pour des combinaisons spécifiques de colonnes.

### Requête :
```sql
SELECT
     DATE_TRUNC('day',order_date) as truncated_date,
    customer_id,
    product_id,
    SUM(price) AS total_sales
FROM
    orders
JOIN
    order_items ON orders.id = order_items.order_id
GROUP BY
    GROUPING SETS (( DATE_TRUNC('day',order_date), customer_id), (customer_id, product_id), ( DATE_TRUNC('day',order_date)), ())
ORDER BY truncated_date DESC;
```

### Explication :
- `(order_date, customer_id)` : Total des ventes par date et client.
- `(customer_id, product_id)` : Total des ventes par client et produit.
- `(order_date)` : Total des ventes par date.
- `()` : Total global (toutes les ventes).

### Exemple de Résultat :
| order_date | customer_id | product_id | total_sales |
|------------|-------------|------------|-------------|
| 2024-11-01 | 1           | NULL       | 200.00      |
| 2024-11-01 | NULL        | NULL       | 400.00      |
| NULL       | 1           | 101        | 100.00      |
| NULL       | 2           | 102        | 50.00       |
| NULL       | NULL        | NULL       | 500.00      |

### Points Clés :
- Les lignes avec `NULL` dans les colonnes non utilisées indiquent des totaux partiels ou globaux.
- C’est le plus flexible des trois.

---

## 2. ROLLUP

### Description :
- Permet de calculer des totaux cumulés hiérarchiques.
- Utile pour obtenir des totaux et sous-totaux à plusieurs niveaux.

### Requête :
```sql
SELECT
    DATE_TRUNC('day', order_date) AS truncated_date,
    customer_id,
    SUM(price) AS total_sales
FROM
    orders
JOIN
    order_items ON orders.id = order_items.order_id
GROUP BY
    ROLLUP (DATE_TRUNC('day', order_date), customer_id)
ORDER BY truncated_date DESC;
```

### Explication :
- Crée des totaux dans cet ordre hiérarchique :
  1. Par `order_date` et `customer_id`.
  2. Par `order_date` (tous les clients d'une date).
  3. Total global (toutes les dates et tous les clients).

### Exemple de Résultat :
| order_date | customer_id | total_sales |
|------------|-------------|-------------|
| 2024-11-01 | 1           | 200.00      |
| 2024-11-01 | 2           | 100.00      |
| 2024-11-01 | NULL        | 300.00      |
| 2024-11-02 | 1           | 150.00      |
| 2024-11-02 | NULL        | 150.00      |
| NULL       | NULL        | 450.00      |

### Points Clés :
- La hiérarchie est importante. Les totaux partiels sont toujours calculés du plus détaillé vers le plus global.
- Plus simple que `GROUPING SETS` mais moins flexible.

---

## 3. CUBE

### Description :
- Génère toutes les combinaisons possibles de colonnes pour les totaux.
- Utile pour obtenir des analyses multidimensionnelles.

### Requête :
```sql
SELECT
     DATE_TRUNC('day',order_date) as truncated_date,
    customer_id,
    product_id,
    SUM(price) AS total_sales
FROM
    orders
JOIN
    order_items ON orders.id = order_items.order_id
GROUP BY
    CUBE ( DATE_TRUNC('day',order_date), customer_id, product_id)
ORDER BY truncated_date DESC;
```

### Explication :
- Produit des totaux pour toutes les combinaisons :
  - Chaque colonne seule.
  - Toutes les paires de colonnes.
  - Toutes les colonnes combinées.
  - Total global.

### Exemple de Résultat :
| order_date | customer_id | product_id | total_sales |
|------------|-------------|------------|-------------|
| 2024-11-01 | 1           | 101        | 100.00      |
| 2024-11-01 | 1           | NULL       | 200.00      |
| 2024-11-01 | NULL        | 101        | 150.00      |
| NULL       | 1           | 101        | 100.00      |
| NULL       | NULL        | NULL       | 500.00      |

### Points Clés :
- Produit un nombre plus élevé de lignes que `GROUPING SETS` et `ROLLUP`.
- Très utile pour des analyses complexes avec plusieurs dimensions.

---

## Résumé des Différences :

| **Fonction**       | **Usage**                                           | **Flexibilité**  | **Nombre de Lignes Générées** |
|---------------------|-----------------------------------------------------|------------------|-------------------------------|
| **GROUPING SETS**   | Totaux pour des groupes spécifiques de colonnes.    | Très flexible    | Dépend des groupes définis.  |
| **ROLLUP**          | Totaux hiérarchiques basés sur l'ordre des colonnes.| Moins flexible   | Moins de lignes.             |
| **CUBE**            | Totaux pour toutes les combinaisons de colonnes.    | Moins flexible   | Beaucoup plus de lignes.     |

---

Ces exemples offrent une vue claire et progressive de l'utilisation des agrégats complexes en SQL pour différentes situations.
