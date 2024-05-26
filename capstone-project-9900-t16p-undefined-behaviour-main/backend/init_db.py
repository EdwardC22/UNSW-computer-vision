import psycopg2
import config

conn = psycopg2.connect(
        host="localhost",
        database="orderup",
        user = config.DB_USERNAME,
        password = config.DB_PASSWORD)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS managers CASCADE;')
cur.execute('CREATE TABLE managers (id SERIAL PRIMARY KEY NOT NULL,'
                                    'username varchar (30) UNIQUE NOT NULL,'
                                    'email varchar (300) UNIQUE NOT NULL,'
                                    'password varchar (256) NOT NULL);'
                                )

cur.execute('DROP TABLE IF EXISTS restaurants CASCADE;')
cur.execute('CREATE TABLE restaurants (id SERIAL PRIMARY KEY,'
                                    'name varchar (150) UNIQUE NOT NULL);'
                                )

cur.execute('DROP TABLE IF EXISTS managers_restaurants CASCADE;')
cur.execute('CREATE TABLE managers_restaurants (manager_id int REFERENCES managers(id),'
                                    'restaurant_id int REFERENCES restaurants(id));'
                                )

cur.execute('DROP TABLE IF EXISTS categories CASCADE;')
cur.execute('CREATE TABLE categories (id SERIAL PRIMARY KEY,'
                                    'name varchar (150) NOT NULL,'
                                    'restaurant_id int REFERENCES restaurants(id),'
                                    'restaurant_pos int NOT NULL);'
                                 )

cur.execute('DROP TABLE IF EXISTS items CASCADE;')
cur.execute('CREATE TABLE items (id SERIAL PRIMARY KEY,'
                                    'name varchar (150) NOT NULL,'
                                    'description varchar (300),'
                                    'ingredients varchar (300),'
                                    'image text,'
                                    'cost numeric (7,2) NOT NULL,'
                                    'category_pos int NOT NULL,'
                                    'active boolean NOT NULL DEFAULT true);'
                                 )

cur.execute('DROP TABLE IF EXISTS items_categories CASCADE;')
cur.execute('CREATE TABLE items_categories (item_id int REFERENCES items(id) ON DELETE CASCADE,'
                                    'category_id int REFERENCES categories(id) ON DELETE CASCADE);'
                                 )

cur.execute('DROP TABLE IF EXISTS tables CASCADE;')
cur.execute('CREATE TABLE tables (id SERIAL PRIMARY KEY,'
                                    'number int NOT NULL,'
                                    'restaurant_id int REFERENCES restaurants(id),'
                                    'active boolean NOT NULL DEFAULT true);'
                                 )

cur.execute('DROP TABLE IF EXISTS orders CASCADE;')
cur.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY,'
                                    'table_id int REFERENCES tables(id),'
                                    'submit_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,'
                                    'paid boolean DEFAULT false,'
                                    'total_cost numeric (15,2) DEFAULT 0.00,'
                                    'restaurant_id int REFERENCES restaurants(id));'
                                    )

cur.execute('DROP TABLE IF EXISTS status CASCADE;')
cur.execute('CREATE TABLE status (id int PRIMARY KEY,'
                                    'value varchar (150) NOT NULL);'
                                 )

cur.executemany('INSERT INTO status (id, value) VALUES (%s, %s)', [(0,'Received'), (1, 'In progress'), (2, 'Complete'), (3, 'Delivered')])

cur.execute('DROP TABLE IF EXISTS order_items CASCADE;')
cur.execute('CREATE TABLE order_items (id SERIAL PRIMARY KEY,'
                                    'order_id int REFERENCES orders(id),'
                                    'item_id int REFERENCES items(id),'
                                    'item_cost numeric (7,2) NOT NULL,'
                                    'quantity int NOT NULL,'
                                    'status int REFERENCES status(id),'
                                    'completion_time TIMESTAMP WITH TIME ZONE,'
                                    'delivery_time TIMESTAMP WITH TIME ZONE);'
                                 )

cur.execute('DROP TABLE IF EXISTS assistance CASCADE;')
cur.execute('CREATE TABLE assistance (id SERIAL PRIMARY KEY,'
                                    'table_id int REFERENCES tables(id),'
                                    'bill boolean NOT NULL,'
                                    'complete boolean NOT NULL DEFAULT false,'
                                    'submit_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP);'
                                 )

conn.commit()

cur.close()
conn.close()
