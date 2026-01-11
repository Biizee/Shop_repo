import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    );

""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers ( 
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );

""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders ( 
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        order_date DATE NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

""")

#cursor.execute("""
#    INSERT INTO products (name, category, price) VALUES
#        ('iPhone 14', 'смартфони', 1000.00),
#        ('Samsung Galaxy S23', 'смартфони', 900.00),
#        ('Dell XPS 13', 'ноутбуки', 1200.00),
#        ('MacBook Air', 'ноутбуки', 1100.00),
#        ('iPad Pro', 'планшети', 800.00),
#        ('Samsung Tab S8', 'планшети', 700.00),
#        ('Sony WH-1000XM5', 'навушники', 350.00);
#               
#""")
#
#cursor.execute("""
#    INSERT INTO customers (first_name, last_name, email) VALUES
#        ('Іван', 'Петренко', 'ivan.petrenko@example.com'),
#        ('Марія', 'Сидоренко', 'maria.sydorenko@example.com'),
#        ('Олексій', 'Коваленко', 'oleksiy.kovalenko@example.com'),
#        ('Анна', 'Іваненко', 'anna.ivanenko@example.com');
#
#""")
#
#cursor.execute("""
#    INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES
#        (1, 1, 2, '2026-01-01'),
#        (2, 3, 1, '2026-01-02'),
#        (1, 5, 3, '2026-01-03'),
#        (3, 2, 1, '2026-01-04'),
#        (4, 7, 4, '2026-01-05'),
#        (2, 4, 1, '2026-01-06'),
#        (3, 6, 2, '2026-01-07');
#
#""")
#
#conn.commit()

def total_price():
    cursor.execute("""
        SELECT SUM(orders.quantity * products.price)
        FROM orders
        INNER JOIN products ON orders.product_id = products.product_id
    """)
    result = cursor.fetchone()[0]
    print(f"\nЗагальний обсяг продажів - {result}")


def total_orders_per_customer():
    cursor.execute("""
        SELECT customers.first_name, customers.last_name, COUNT(orders.order_id)
        FROM customers
        INNER JOIN orders ON customers.customer_id = orders.customer_id
        GROUP BY customers.customer_id
    """)
    result = cursor.fetchall()
    for r in result:
        if r[2] == 1:
            print(f"Користувач {r[0]} {r[1]} купив(ла) {r[2]} товар" )
        else:
            print(f"Користувач {r[0]} {r[1]} купив(ла) {r[2]} товарів" )


def avarage_price():
    cursor.execute("""
        SELECT AVG(orders.quantity * products.price)
        FROM orders
        INNER JOIN products ON orders.product_id = products.product_id
    """)
    result = cursor.fetchone()[0]
    print(f"\nСередній чек замовлення - {round(result,2)}")


def popular_category():
    cursor.execute("""
        SELECT products.category, SUM(orders.quantity)
        FROM orders
        INNER JOIN products ON products.product_id = orders.product_id
        GROUP BY products.category
        ORDER BY SUM(orders.quantity) DESC
        LIMIT 1
    """)
    result = cursor.fetchone()[0]
    print(f"\nНайбільш популярна категорія - {result}")

def total_products_per_category():
    cursor.execute("""
        SELECT category, COUNT(product_id)
        FROM products
        GROUP BY category
    """)
    result = cursor.fetchall()
    for r in result:
        print(f"{r[0]} - {r[1]}")


while True:
    
    print("""\n------------------------------------------------------------
1. Загальний обсяг продажів (сума) за ісі замовлення.
2. Кількість замовлень для кожного клієнта.
3. Середній чек замовлення.
4. Найбільш популярна категорія товарів.
5. Загальна кількість товарів кожної категорії.
6. Оновлення цін (ціни на смартфони збільшаться на 10%).
7. Завершити роботу.
------------------------------------------------------------\n""")
    
    choice = int(input("Ваш вибір:\n"))
    
    if choice == 7:
        break
    
    elif choice == 1:
        total_price()
    
    elif choice == 2:
        total_orders_per_customer()
    
    elif choice == 3:
        avarage_price()
    
    elif choice == 4:
        popular_category()
    
    elif choice == 5:
        total_products_per_category()
