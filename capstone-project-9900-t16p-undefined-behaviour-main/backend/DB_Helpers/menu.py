def getRestaurant(cur, restaurantName):
    cur.execute('SELECT * FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    return {'id': result[0], 'name': result[1]}

def getCategoriesRestaurant(cur, restaurantName):
    cur.execute('SELECT c.id, c.name, c.restaurant_pos FROM categories c, restaurants r '
                'WHERE c.restaurant_id = r.id AND r.name = %s ORDER BY c.restaurant_pos',
                (restaurantName,))
    result = cur.fetchall()
    categories = [{'id': category[0], 'name': category[1], 'restaurant_pos': category[2]} for category in result]
    return categories

def getItemsCategory(cur, categoryID, popularItems):
    cur.execute('SELECT i.id, i.name, i.description, i.ingredients, i.image, i.cost, i.category_pos '
                'FROM items i, items_categories ic '
                'WHERE ic.category_id = %s AND ic.item_id = i.id '
                'ORDER BY i.category_pos',
                (categoryID,)
                )
    result = cur.fetchall()
    items = [{'id': item[0], 'name': item[1], 'description': item[2],
              'ingredients': item[3], 'image':item[4], 'cost': item[5],
              'category_pos': item[6], 'popular':(item[0] in popularItems)} for item in result]
    return items

def getTables(cur, restaurantName):
    cur.execute('SELECT MAX(number) FROM tables t, restaurants r '
                'WHERE t.restaurant_id = r.id AND r.name = %s AND t.active = true',
                (restaurantName,))
    tables = cur.fetchone()[0]
    return tables

def updateTables(cur, restaurantName, newTables):
    newTable = newTables.get('tables')
    if not newTable or newTable < 1:
        return None
    cur.execute('SELECT id FROM restaurants WHERE name = %s',
                (restaurantName,))
    found = cur.fetchone()
    if not found:
        return None
    restaurantID = found[0]
    cur.execute('SELECT MAX(number) FROM tables WHERE restaurant_id = %s AND active = true',
                (restaurantID,))
    activeTables = cur.fetchone()[0]
    if newTable > activeTables:
        cur.execute('UPDATE tables SET active = true WHERE restaurant_id = %s AND active = false AND number <= %s', 
                    (restaurantID, newTable))
        activeTables += cur.rowcount
        if newTable > activeTables:
            cur.executemany('INSERT INTO tables (number, restaurant_id)'
                            'VALUES (%s, %s)', [(i + 1, restaurantID) for i in range(activeTables, newTable)])
            if not cur.rowcount == newTable - activeTables:
                return None
    else:
        cur.execute('UPDATE tables SET active = false WHERE restaurant_id = %s AND number > %s',
                        (restaurantID, newTable))
        if not cur.rowcount == activeTables-newTable:
            return None
    return newTable

def addItem(cur, newItem):
    name = newItem.get('name')
    description = newItem.get('description')
    ingredients = newItem.get('ingredients')
    image = newItem.get('image')
    cost = newItem.get('cost')
    categoryID = newItem.get('categoryID')
    if not name or not cost or not categoryID:
        return None
    # Find the next position
    cur.execute('SELECT COUNT(*) FROM items_categories ic '
                'WHERE ic.category_id = %s', 
                (categoryID,))
    position = cur.fetchone()[0] + 1
    cur.execute('INSERT INTO items (name, description, ingredients, image, cost, category_pos)'
                'VALUES (%s, %s, %s, %s, %s, %s) RETURNING id',
                (name, description, ingredients, image, float(cost), position))
                
    if not cur.rowcount:
        return None
    itemID = cur.fetchone()[0]
    cur.execute('INSERT INTO items_categories (item_id, category_id)'
                'VALUES (%s, %s)',
                (itemID, categoryID)
                )
    if not cur.rowcount:
        return None
    return itemID

def addCategory(cur, restaurantName, newCategory):
    cur.execute('SELECT id FROM restaurants WHERE name = %s',
                (restaurantName,))
    found = cur.fetchone()
    if not found:
        return None
    restaurantID = found[0]
    name = newCategory.get('name')
    if not name:
        return None
    # Find the next position
    cur.execute('SELECT COUNT(*) FROM categories WHERE restaurant_id = %s', 
                (restaurantID,))
    position = cur.fetchone()[0] + 1
    cur.execute('INSERT INTO categories (name, restaurant_id, restaurant_pos)'
                'VALUES (%s, %s, %s) RETURNING id', (name, restaurantID, position,))
    if not cur.rowcount:
        return None
    return cur.fetchone()[0]

def getItem(cur, itemID):
    cur.execute('SELECT * FROM items WHERE id = %s', (itemID,))
    result = cur.fetchone()
    if not result:
        return None
    item = {'id': result[0], 'name': result[1], 'description': result[2],
            'ingredients': result[3], 'image': result[4], 'cost': result[5], 
            'category_pos': result[6]}
    return item

def getCategory(cur, categoryID):
    cur.execute('SELECT * FROM categories WHERE id = %s', (categoryID,))
    result = cur.fetchone()
    if not result:
        return None
    category = {'id': result[0], 'name': result[1], 'restaurant_pos': result[2]}
    return category

def updateItem(cur, itemID, item):
    name = item.get('name')
    description = item.get('description')
    ingredients = item.get('ingredients')
    image = item.get('image')
    cost = item.get('cost')
    if not name or not cost:
        return None
    cur.execute('UPDATE items SET name = %s, description = %s, '
                'ingredients = %s, image = %s, cost = %s WHERE id = %s RETURNING *', 
                (name, description, ingredients, image, float(cost), itemID))
    if not cur.rowcount:
        return None
    return itemID

def updateItemPos(cur, itemID, positions):
    # Obtain the category
    cur.execute('SELECT category_id FROM items_categories WHERE item_id = %s', (itemID,))
    result = cur.fetchone()
    if not result:
        return None
    categoryID = result[0]
    # Obtain the old position
    cur.execute('SELECT category_pos FROM items WHERE id = %s', (itemID,))
    result = cur.fetchone()
    if not result:
        return None
    oldPosition = result[0]
    if not positions.get('new_position'):
        return None
    newPosition = int(positions.get('new_position'))
    # Shift all other items to the right
    if newPosition < oldPosition:
        cur.execute('UPDATE items SET category_pos = category_pos + 1 FROM items_categories ic '
                    'WHERE category_pos >= %s AND category_pos < %s AND id = ic.item_id AND ' 
                    'ic.category_id = %s', (newPosition, oldPosition, categoryID))
        if not cur.rowcount == oldPosition - newPosition:
            return None
    # Shift all other items to the left
    else:
        cur.execute('UPDATE items SET category_pos = category_pos - 1 FROM items_categories ic '
                    'WHERE category_pos > %s AND category_pos <= %s AND id = ic.item_id AND ' 
                    'ic.category_id = %s', (oldPosition, newPosition, categoryID))
        if not cur.rowcount == newPosition - oldPosition:
            return None
    # Update the item's position
    cur.execute('UPDATE items SET category_pos = %s WHERE id = %s', (newPosition, itemID))
    return itemID

def updateItemCategory(cur, itemID, categories):
    # Obtain the old category
    cur.execute('SELECT category_id FROM items_categories WHERE item_id = %s', (itemID,))
    result = cur.fetchone()
    if not result:
        return None
    oldCategory = result[0]
    newCategory = categories.get('new_category')
    if not newCategory:
        return None
    # Obtain the old position
    cur.execute('SELECT category_pos FROM items WHERE id = %s', (itemID,))
    result = cur.fetchone()
    if not result:
        return None
    position = result[0]
    # Shift remaining items to the left
    cur.execute('UPDATE items SET category_pos = category_pos - 1 FROM items_categories ic '
                'WHERE category_pos > %s AND id = ic.item_id AND ic.category_id = %s',
                (position, oldCategory))
    # Update the category
    cur.execute('UPDATE items_categories SET category_id = %s WHERE item_id = %s',
                (newCategory, itemID))
    # Find the next position in the new category
    cur.execute('SELECT COUNT(*) FROM items i, items_categories ic '
                'WHERE ic.category_id = %s AND ic.item_id = i.id ', 
                (newCategory,))
    position = cur.fetchone()[0]
    # Update the item's position
    cur.execute('UPDATE items SET category_pos = %s WHERE id = %s', (position, itemID))
    return itemID

def updateCategory(cur, categoryID, category):
    name = category.get('name')
    if not name:
        return None
    cur.execute('UPDATE categories SET name = %s WHERE id = %s RETURNING *', 
                (name, categoryID))
    if not cur.rowcount:
        return None
    return categoryID

def updateCategoryPos(cur, categoryID, positions):
    # Obtain the restaurantID
    cur.execute('SELECT restaurant_id, restaurant_pos FROM categories WHERE id = %s', (categoryID,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]
    oldPosition = result[1]
    if not positions.get('new_position'):
        return None
    newPosition = int(positions.get('new_position'))
    # Shift all other categories to the right
    if newPosition < oldPosition:
        cur.execute('UPDATE categories SET restaurant_pos = restaurant_pos + 1 '
                    'WHERE restaurant_pos >= %s AND restaurant_pos < %s AND restaurant_id = %s', 
                    (newPosition, oldPosition, restaurantID)) 
        if not cur.rowcount == oldPosition - newPosition:
            return None
    # Shift all other categories to the left
    else:
        cur.execute('UPDATE categories SET restaurant_pos = restaurant_pos - 1 '
                    'WHERE restaurant_pos > %s AND restaurant_pos <= %s AND restaurant_id = %s',
                    (oldPosition, newPosition, restaurantID))
        if not cur.rowcount == newPosition - oldPosition:
            return None
    # Update the category's position
    cur.execute('UPDATE categories SET restaurant_pos = %s WHERE id = %s', (newPosition, categoryID))
    return categoryID

def removeItem(cur, itemID):
    # Obtain the position
    cur.execute('SELECT category_pos FROM items WHERE id = %s', (itemID,))
    result = cur.fetchone()
    if not result:
        return None
    position = result[0]
    # Obtain the category
    cur.execute('SELECT category_id FROM items_categories WHERE item_id = %s', (itemID,))
    result = cur.fetchone()
    if not result:
        return None
    categoryID = result[0]
    # Shift remaining items to the left
    cur.execute('UPDATE items SET category_pos = category_pos - 1 FROM items_categories ic '
                'WHERE category_pos > %s AND id = ic.item_id AND ic.category_id = %s',
                (position, categoryID))
    # Set the item to inactive
    cur.execute('UPDATE items SET active = false WHERE id = %s', (itemID,))
    if not cur.rowcount:
        return None
    # Remove the item from its category
    cur.execute('DELETE FROM items_categories WHERE item_id = %s',
                (itemID,))
    if not cur.rowcount:
        return None
    return itemID

def removeCategory(cur, categoryID):
    # Obtain the restaurantID and position
    cur.execute('SELECT restaurant_id, restaurant_pos FROM categories WHERE id = %s', (categoryID,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]
    position = result[1]
    # Shift remaining categories to the left
    cur.execute('UPDATE categories SET restaurant_pos = restaurant_pos - 1 '
                'WHERE restaurant_pos > %s AND restaurant_id = %s',
                (position, restaurantID))
    # Set items in the category to inactive
    cur.execute('UPDATE items SET active = false FROM items_categories ic WHERE id = ic.item_id '
                'AND ic.category_id = %s', (categoryID,))
    # Delete the category
    cur.execute('DELETE FROM categories WHERE id = %s RETURNING *',
                (categoryID,))
    if not cur.rowcount:
        return None
    return categoryID
