import psycopg2
from psycopg2 import sql
from faker import Faker
import random

# Connexion à la base de données
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="ecommerce_db",
    user="ecommerce_user",
    password="ecommerce_password"
)
cursor = conn.cursor()

# Instance de Faker
fake = Faker('fr_FR')

# Génération des clients
print("Génération des clients...")
num_customers = 100000
customer_ids = []
for _ in range(num_customers):
    name = fake.name()
    email = fake.unique.email()
    created_at = fake.date_time_this_year()
    cursor.execute("""
        INSERT INTO customers (name, email, created_at)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (name, email, created_at))
    customer_id = cursor.fetchone()[0]
    customer_ids.append(customer_id)

# Génération des fournisseurs
print("Génération des fournisseurs...")
num_suppliers = 10000
supplier_ids = []
for _ in range(num_suppliers):
    name = fake.company()
    contact_name = fake.name()
    contact_email = fake.email()
    phone = fake.phone_number()
    address = fake.address()
    city = fake.city()
    country = fake.country()
    created_at = fake.date_time_this_year()
    cursor.execute("""
        INSERT INTO suppliers (name, contact_name, contact_email, phone, address, city, country, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (name, contact_name, contact_email, phone, address, city, country, created_at))
    supplier_id = cursor.fetchone()[0]
    supplier_ids.append(supplier_id)

# Génération des catégories
print("Génération des catégories...")
num_categories = 500
category_ids = []
for _ in range(num_categories):
    name = fake.unique.word().capitalize()
    description = fake.text()
    created_at = fake.date_time_this_year()
    cursor.execute("""
        INSERT INTO categories (name, description, created_at)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (name, description, created_at))
    category_id = cursor.fetchone()[0]
    category_ids.append(category_id)

# Génération des produits
print("Génération des produits...")
num_products = 50000
product_ids = []
for _ in range(num_products):
    name = fake.word().capitalize() + ' ' + fake.word().capitalize()
    description = fake.text()
    price = round(random.uniform(5.0, 1000.0), 2)
    stock_quantity = random.randint(0, 1000)
    created_at = fake.date_time_this_year()
    category_id = random.choice(category_ids)
    supplier_id = random.choice(supplier_ids)
    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, created_at, category_id, supplier_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (name, description, price, stock_quantity, created_at, category_id, supplier_id))
    product_id = cursor.fetchone()[0]
    product_ids.append(product_id)

# Génération des commandes
print("Génération des commandes...")
num_orders = 200000
order_ids = []
for _ in range(num_orders):
    customer_id = random.choice(customer_ids)
    order_date = fake.date_time_this_year()
    cursor.execute("""
        INSERT INTO orders (customer_id, order_date)
        VALUES (%s, %s)
        RETURNING id
    """, (customer_id, order_date))
    order_id = cursor.fetchone()[0]
    order_ids.append(order_id)

# Génération des éléments de commande
print("Génération des éléments de commande...")
order_item_ids = []
for order_id in order_ids:
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 10)
        price = round(random.uniform(5.0, 1000.0), 2)
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (order_id, product_id, quantity, price))
        order_item_id = cursor.fetchone()[0]
        order_item_ids.append(order_item_id)

# Génération des avis
print("Génération des avis...")
num_reviews = 50000
for _ in range(num_reviews):
    product_id = random.choice(product_ids)
    customer_id = random.choice(customer_ids)
    rating = random.randint(1, 5)
    comment = fake.text()
    review_date = fake.date_time_this_year()
    cursor.execute("""
        INSERT INTO reviews (product_id, customer_id, rating, comment, review_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (product_id, customer_id, rating, comment, review_date))

# Génération des paiements
print("Génération des paiements...")
payment_methods = ['Carte de crédit', 'PayPal', 'Virement bancaire', 'Paiement à la livraison']
for order_id in order_ids:
    payment_date = fake.date_time_this_year()
    amount = round(random.uniform(10.0, 2000.0), 2)
    payment_method = random.choice(payment_methods)
    cursor.execute("""
        INSERT INTO payments (order_id, payment_date, amount, payment_method)
        VALUES (%s, %s, %s, %s)
    """, (order_id, payment_date, amount, payment_method))

# Génération des expéditions
print("Génération des expéditions...")
shipping_methods = ['Standard', 'Express', 'Overnight']
shipping_statuses = ['En attente', 'Expédié', 'Livré', 'Annulé']
for order_id in order_ids:
    shipping_date = fake.date_time_this_year()
    shipping_method = random.choice(shipping_methods)
    tracking_number = fake.uuid4()
    status = random.choice(shipping_statuses)
    cursor.execute("""
        INSERT INTO shippings (order_id, shipping_date, shipping_method, tracking_number, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (order_id, shipping_date, shipping_method, tracking_number, status))

# Génération des listes de souhaits
print("Génération des listes de souhaits...")
wishlist_ids = []
for customer_id in customer_ids:
    created_at = fake.date_time_this_year()
    cursor.execute("""
        INSERT INTO wishlists (customer_id, created_at)
        VALUES (%s, %s)
        RETURNING id
    """, (customer_id, created_at))
    wishlist_id = cursor.fetchone()[0]
    wishlist_ids.append(wishlist_id)

# Génération des éléments des listes de souhaits
print("Génération des éléments des listes de souhaits...")
for wishlist_id in wishlist_ids:
    num_items = random.randint(1, 10)
    products_in_wishlist = random.sample(product_ids, num_items)
    for product_id in products_in_wishlist:
        added_at = fake.date_time_this_year()
        cursor.execute("""
            INSERT INTO wishlist_items (wishlist_id, product_id, added_at)
            VALUES (%s, %s, %s)
        """, (wishlist_id, product_id, added_at))

# Génération des paniers
print("Génération des paniers...")
cart_ids = []
for customer_id in customer_ids:
    created_at = fake.date_time_this_year()
    cursor.execute("""
        INSERT INTO carts (customer_id, created_at)
        VALUES (%s, %s)
        RETURNING id
    """, (customer_id, created_at))
    cart_id = cursor.fetchone()[0]
    cart_ids.append(cart_id)

# Génération des éléments des paniers
print("Génération des éléments des paniers...")
for cart_id in cart_ids:
    num_items = random.randint(1, 5)
    products_in_cart = random.sample(product_ids, num_items)
    for product_id in products_in_cart:
        quantity = random.randint(1, 5)
        added_at = fake.date_time_this_year()
        cursor.execute("""
            INSERT INTO cart_items (cart_id, product_id, quantity, added_at)
            VALUES (%s, %s, %s, %s)
        """, (cart_id, product_id, quantity, added_at))

# Génération des retours
print("Génération des retours...")
return_reasons = ['Défectueux', 'Non conforme', 'Mauvais article', 'Changement d\'avis']
return_statuses = ['En attente', 'Traitée', 'Rejetée']
num_returns = int(len(order_item_ids) * 0.1)  # 10% des éléments commandés sont retournés
returned_order_item_ids = random.sample(order_item_ids, num_returns)
for order_item_id in returned_order_item_ids:
    return_date = fake.date_time_this_year()
    reason = random.choice(return_reasons)
    status = random.choice(return_statuses)
    cursor.execute("""
        INSERT INTO returns (order_item_id, return_date, reason, status)
        VALUES (%s, %s, %s, %s)
    """, (order_item_id, return_date, reason, status))

# Génération des promotions
print("Génération des promotions...")
num_promotions = 200
promotion_ids = []
for _ in range(num_promotions):
    name = fake.catch_phrase()
    description = fake.text()
    discount_percentage = round(random.uniform(5.0, 50.0), 2)
    start_date = fake.date_time_this_year()
    end_date = fake.date_time_between_dates(datetime_start=start_date)
    cursor.execute("""
        INSERT INTO promotions (name, description, discount_percentage, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (name, description, discount_percentage, start_date, end_date))
    promotion_id = cursor.fetchone()[0]
    promotion_ids.append(promotion_id)

# Association des promotions aux produits
print("Association des promotions aux produits...")
for promotion_id in promotion_ids:
    num_products_in_promotion = random.randint(5, 20)
    products_in_promotion = random.sample(product_ids, num_products_in_promotion)
    for product_id in products_in_promotion:
        cursor.execute("""
            INSERT INTO product_promotions (product_id, promotion_id)
            VALUES (%s, %s)
        """, (product_id, promotion_id))

# Validation des transactions
conn.commit()
cursor.close()
conn.close()
print("Données insérées avec succès !")
