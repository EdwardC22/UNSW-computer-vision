import psycopg2, base64, datetime, config
from werkzeug.security import generate_password_hash
from random import randint

conn = psycopg2.connect(
        host="localhost",
        database="orderup",
        user = config.DB_USERNAME,
        password = config.DB_PASSWORD)

cur = conn.cursor()

# Create a restaurant
username = config.DUMMY_USERNAME
email = config.DUMMY_EMAIL
password = generate_password_hash(config.DUMMY_PASSWORD, method='sha256')
restaurantName = config.DUMMY_RESTAURANT
cur.execute('INSERT INTO managers (username, email, password)'
            'VALUES (%s, %s, %s) RETURNING id', (username, email, password))
managerID = cur.fetchone()[0]
cur.execute('INSERT INTO restaurants (name) VALUES (%s) RETURNING id',
            (restaurantName,))
restaurantID = cur.fetchone()[0]
cur.execute('INSERT INTO managers_restaurants (manager_id, restaurant_id)'
            'VALUES (%s, %s)', (managerID, restaurantID))
cur.executemany('INSERT INTO tables (number, restaurant_id)'
            'VALUES (%s, %s)', [(i, restaurantID) for i in range(1,16)])

# Create categories
categoryNames = ['Breakfast', 'Lunch', 'Dinner']
categoryIDs = []
for i in range(3):
    cur.execute('INSERT INTO categories (name, restaurant_id, restaurant_pos)'
                'VALUES (%s, %s, %s) RETURNING id', (categoryNames[i], restaurantID, i+1))
    categoryID = cur.fetchone()[0]
    categoryIDs.append(categoryID)

# Create Items
categoryItems = [[['Avocado Toast', 'Toast with avocado', 'Avocado, bread', 'AvocadoToast.jpg', 10.50], 
                  ['Banana Smoothie', 'Creamy delicious smoothie', 'Banana, milk, yoghurt, honey', 'BananaSmoothie.jpg', 8.50],
                  ['Cereal', 'Crunchy', 'Corn flakes, milk', 'Cereal.jpg', 6.75],
                  ['Eggs on Toast', 'Runny eggs on sourdough bread', 'Eggs, bread, parsley', 'Eggs.jpg', 12.30],
                  ['French Toast', 'Sweet french toast', 'Eggs, bread, sugar, berries', 'FrenchToast.jpg', 15.80]],
                 [['Minestrone Soup', 'Hearty vegetable soup', 'Carrots, celery, potato, tomato, pasta', 'Minestrone.jpg', 15.35],
                  ['Sushi', 'Fresh salmon and avocado roll', 'Salmon, rice, avocado, soy sauce', 'Sushi.jpg', 14.00],
                  ['Fried Noodles', 'Tasty stir fried noodles with egg', 'Noodles, sesame seeds, egg, bok choy', 'Noodles.jpg', 17.00],
                  ['Burger', 'Classic beef burger', 'Bread, beef patty, tomato, lettuce, onion, BBQ sauce', 'Burger.jpg', 10.00],
                  ['Pizza', 'Simple tomato pizza with mozzarella', 'Dough base, mozzarella, tomato, basil', 'Pizza.jpg', 21.30]],
                 [['Spaghetti', 'Tasty spaghetti bolognaise', 'Pasta, beef, tomato, cheese', 'Spaghetti.jpg', 22.00],
                  ['Salmon', 'Healthy pan fried salmon', 'Salmon, brocolini', 'Salmon.jpg', 23.50],
                  ['Steak', 'Cooked to your preference', 'Beef, onion, thyme', 'Steak.jpg', 25.00],
                  ['Stew', 'Slow cooked beef, potato and carrot stew', 'Beef, potato, carrot, onion', 'Stew.jpg', 19.90],
                  ['Tacos', 'Fresh beef tacos', 'Tacos, beef, cheese, onion, lime, corriander', 'Taco.jpg', 18.70]]]
itemIDs = []
itemTimes = []
itemPop = []
for i in range(3):
    categoryID = categoryIDs[i]
    for j in range(len(categoryItems[i])):
        item = categoryItems[i][j]
        name = item[0]
        description = item[1]
        ingredients = item[2]
        with open('dummyImages/' + item[3], "rb") as img_file:
            image = base64.b64encode(img_file.read())
        cost = item[4]
        cur.execute('INSERT INTO items (name, description, ingredients, image, cost, category_pos)'
                    'VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
                    (name, description, ingredients, 'data:image/jpeg;base64,' + image.decode('utf-8'), cost, j+1))
        itemID = cur.fetchone()[0]
        cur.execute('INSERT INTO items_categories (item_id, category_id)'
                    'VALUES (%s, %s)',
                    (itemID, categoryID)
                    )
        itemIDs.append(itemID)
        itemTimes.append(randint(5,30))
        itemPop.append(randint(0,2))

# Create Orders
cur.execute('SELECT id FROM tables WHERE restaurant_id = %s', (restaurantID,))
tableIDs = [table[0] for table in cur.fetchall()]
today = datetime.date.today()
for i in range(30):
    date = today - datetime.timedelta(days=i)
    for table in tableIDs:
        for j in range(16):
            for k in range(2):
                if k == 1 and j not in [5, 6, 11, 12, 13]:
                    continue
                hourSelect = randint(0,1)
                if not hourSelect:
                    continue
                orderMin = randint(0,59)
                time = datetime.time(hour=7+j, minute=orderMin, second=0)
                orderTime = datetime.datetime.combine(date, time)
                cur.execute('INSERT INTO orders (table_id, restaurant_id, submit_time, paid) VALUES (%s, %s, %s, %s) RETURNING id',
                            (table, restaurantID, orderTime.strftime("%Y-%m-%d %H:%M:%S"), True))
                orderID = cur.fetchone()[0]
                totalCost = 0
                orderLength = randint(1,len(itemIDs))
                selected = []
                for i in range(orderLength):
                    randIndex = randint(0, len(itemIDs)-1)
                    itemID = itemIDs[randIndex]
                    itemTime = itemTimes[randIndex]
                    if itemID in selected:
                        continue
                    selected.append(itemID)
                    quantity = randint(1,3) + itemPop[randIndex]
                    cur.execute('SELECT i.cost FROM items i WHERE i.id = %s', (itemID,))
                    cost = cur.fetchone()[0]
                    timeVariance = randint(0,30)
                    deliveryTime = orderTime + datetime.timedelta(minutes=(timeVariance+itemTime))
                    cur.execute('INSERT INTO order_items (order_id, item_id, item_cost, quantity, status, delivery_time) '
                                'VALUES (%s, %s, %s, %s, %s, %s)', (orderID, itemID, cost, quantity, 3, deliveryTime.strftime("%Y-%m-%d %H:%M:%S")))
                    totalCost += cost * quantity
                cur.execute('UPDATE orders SET total_cost = %s WHERE id = %s', (totalCost, orderID))

conn.commit()
cur.close()
conn.close()
