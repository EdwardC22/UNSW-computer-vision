# return an array of all orders from a given table within a given restaurant
def getOrder(cur, restaurantName, tableNumber):
    cur.execute('SELECT t.id FROM tables t, restaurants r WHERE t.number = %s AND t.restaurant_id=r.id AND r.name = %s',
                (tableNumber, restaurantName))
    found = cur.fetchone()
    if not found:
        return None
    tableID = found[0]
    cur.execute('SELECT i.name, oi.quantity, s.value, oi.item_cost FROM orders o, order_items oi, items i, status s '
                'WHERE o.paid = false AND o.table_id = %s AND o.id = oi.order_id AND oi.item_id = i.id '
                'AND oi.status = s.id ORDER BY o.submit_time', (tableID,))
    orders = [{'name': order[0], 'quantity': order[1], 'status': order[2], 'cost': order[3]} for order in cur.fetchall()]
    return orders

# Add a given new order to the database of orders for a given table within a given restaurant
def addOrder(cur, restaurantName, tableNumber, newOrder):
    if not newOrder or not len(newOrder):
        return None
    cur.execute('SELECT t.id, t.restaurant_id FROM tables t, restaurants r WHERE t.number = %s AND t.active = true AND '
                't.restaurant_id=r.id AND r.name = %s',
                (tableNumber, restaurantName))
    found = cur.fetchone()
    if not found:
        return None
    tableID = found[0]
    restaurantID = found[1]
    cur.execute('INSERT INTO orders (table_id, restaurant_id) VALUES (%s, %s) RETURNING id', (tableID, restaurantID))
    if not cur.rowcount:
        return None
    orderID = cur.fetchone()[0]

    total_cost = 0
    
    for item in newOrder:
        itemID = item.get('itemID')
        quantity = item.get('quantity')
        if not itemID or not quantity:
            return None
        # Find item cost, ensure item is active and from restaurant
        cur.execute('SELECT i.cost FROM items i, items_categories ic, categories c WHERE i.id = %s AND i.active = true '
                    'AND i.id = ic.item_id AND ic.category_id = c.id AND c.restaurant_id = %s', (itemID, restaurantID))
        found = cur.fetchone()
        if not found:
            return None
        cost = found[0]
        # Add item to the order
        cur.execute('INSERT INTO order_items (order_id, item_id, item_cost, quantity, status) '
                    'VALUES (%s, %s, %s, %s, %s)', (orderID, itemID, cost, quantity, 0))
        if not cur.rowcount:
            return None
        # Update total cost
        total_cost += cost * quantity
    
    cur.execute('UPDATE orders SET total_cost = %s WHERE id = %s', (total_cost, orderID))

    return orderID

# Add an assistance request for a given table within a given restaurant
def addAssistance(cur, restaurantName, tableNumber, assistance):
    bill = assistance.get('bill')
    if bill == None:
        return None
    cur.execute('SELECT t.id FROM tables t, restaurants r WHERE t.number = %s AND t.restaurant_id=r.id AND r.name = %s',
                (tableNumber, restaurantName))
    found = cur.fetchone()
    if not found:
        return None
    tableID = found[0]
    # Ensure there is not a pending request for assistance
    cur.execute('SELECT id FROM assistance WHERE table_id = %s AND complete = false', (tableID,))
    if cur.rowcount:
        return cur.fetchone()[0]
    # If bill is being requested, ensure all order items have been delivered
    if bill:
        cur.execute('SELECT oi.id FROM order_items oi, orders o WHERE oi.order_id=o.id AND o.table_id = %s AND o.paid=false '
                    'AND oi.status!=3', (tableID,))
        if cur.fetchone():
            return None
    cur.execute('INSERT INTO assistance (table_id, bill) VALUES (%s, %s) RETURNING id', (tableID, bill))
    if not cur.rowcount:
        return None
    assistanceID = cur.fetchone()[0]
    # If bill is being paid, update orders to paid
    if bill:
        cur.execute('UPDATE orders SET paid = true WHERE table_id = %s AND paid = false', (tableID,))
    return assistanceID
