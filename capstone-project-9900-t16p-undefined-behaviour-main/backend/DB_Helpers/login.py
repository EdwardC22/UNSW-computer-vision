from werkzeug.security import generate_password_hash, check_password_hash

def getUser(cur, username, email):
    if username:
        cur.execute('SELECT * FROM managers WHERE username = %s', (username,))
        result = cur.fetchone()
        if not result:
            return None
        return {'id': result[0], 'username': result[1], 'email': result[2], 'password': result[3]}
    if email:
        cur.execute('SELECT * FROM managers WHERE email = %s', (email,))
        result = cur.fetchone()
        if not result:
            return None
        return {'id': result[0], 'username': result[1], 'email': result[2], 'password': result[3]}
    return None

def verifyManagerRestaurant(cur, managerID, restaurantName):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return False
    restaurantID = result[0]
    cur.execute('SELECT * from managers_restaurants WHERE manager_id = %s AND restaurant_id = %s',
                (managerID, restaurantID))
    result = cur.fetchone()
    if not result:
        return False
    return True

def verifyPassword(cur, username, password):
    if not password:
        return False
    cur.execute('SELECT password FROM managers WHERE username = %s', (username,))
    result = cur.fetchone()
    if not result:
        return False
    if check_password_hash(result[0], password):
        return True
    else:
        return False

def addUser(cur, credentials):
    username = credentials.get('username')
    email = credentials.get('email')
    password = generate_password_hash(credentials.get('password'), method='sha256')
    restaurantName = credentials.get('restaurant_name')
    cur.execute('INSERT INTO managers (username, email, password)'
                'VALUES (%s, %s, %s) RETURNING id', (username, email, password))
    if not cur.rowcount:
        return None
    managerID = cur.fetchone()[0]
    cur.execute('INSERT INTO restaurants (name) VALUES (%s) RETURNING id',
                (restaurantName,))
    if not cur.rowcount:
        return None
    restaurantID = cur.fetchone()[0]
    cur.execute('INSERT INTO managers_restaurants (manager_id, restaurant_id)'
                'VALUES (%s, %s)', (managerID, restaurantID))
    if not cur.rowcount:
        return None
    # Default number of tables is 10
    cur.executemany('INSERT INTO tables (number, restaurant_id)'
                'VALUES (%s, %s)', [(i, restaurantID) for i in range(1,11)])
    if not cur.rowcount == 10:
        return None
    return managerID
