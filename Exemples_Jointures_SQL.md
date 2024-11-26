
# Exemples de Jointures SQL

## 1. Inner Join (Jointure Interne)

### Requête SQL :
```sql
SELECT
    p.id AS product_id,
    p.name AS product_name,
    s.name AS supplier_name
FROM
    products p
INNER JOIN suppliers s ON p.supplier_id = s.id;
```

### Explication :
- **Inner Join** renvoie uniquement les enregistrements où il y a une correspondance dans les deux tables.
- Dans cet exemple, nous récupérons les produits et leurs fournisseurs correspondants.
- **Seuls les produits qui ont un `supplier_id` correspondant à un `id` dans la table `suppliers` seront inclus dans le résultat.**
- Les produits sans fournisseur (où `supplier_id` est NULL ou ne correspond à aucun fournisseur) ne seront pas affichés.

---

## 2. Left Join (Jointure Gauche)

### Requête SQL :
```sql
SELECT
    p.id AS product_id,
    p.name AS product_name,
    s.name AS supplier_name
FROM
    products p
LEFT JOIN suppliers s ON p.supplier_id = s.id;
```

### Explication :
- **Left Join** renvoie tous les enregistrements de la table de gauche (`products`), ainsi que les enregistrements correspondants de la table de droite (`suppliers`).
- **Si aucun fournisseur correspondant n'est trouvé, les colonnes du fournisseur seront NULL.**
- Cela permet de lister **tous les produits**, y compris ceux qui n'ont pas de fournisseur associé.

---

## 3. Right Join (Jointure Droite)

### Requête SQL :
```sql
SELECT
    p.id AS product_id,
    p.name AS product_name,
    s.name AS supplier_name
FROM
    products p
RIGHT JOIN suppliers s ON p.supplier_id = s.id;
```

### Explication :
- **Right Join** est l'inverse du Left Join.
- Il renvoie tous les enregistrements de la table de droite (`suppliers`), avec les enregistrements correspondants de la table de gauche (`products`).
- **Si aucun produit correspondant n'est trouvé, les colonnes du produit seront NULL.**
- Cela permet de lister **tous les fournisseurs**, y compris ceux qui ne fournissent aucun produit.

---

## 4. Full Outer Join (Jointure Externe Complète)

### Requête SQL :
```sql
SELECT
    p.id AS product_id,
    p.name AS product_name,
    s.name AS supplier_name
FROM
    products p
FULL OUTER JOIN suppliers s ON p.supplier_id = s.id;
```

### Explication :
- **Full Outer Join** combine les résultats des Left Join et Right Join.
- Il renvoie **tous les enregistrements** lorsqu'il y a une correspondance dans l'une ou l'autre des tables.
- **Les enregistrements sans correspondance dans l'une ou l'autre table auront des valeurs NULL pour les colonnes de cette table.**
- Cela permet de voir tous les produits et tous les fournisseurs, y compris :
  - Les produits sans fournisseur.
  - Les fournisseurs sans produit.
