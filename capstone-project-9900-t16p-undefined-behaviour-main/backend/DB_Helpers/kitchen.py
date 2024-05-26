# Marks a given order from a given restaurant from not in progress to in progress
def MarkItemInprogress(cur, restaurantName, orderItemID):
    cur.execute('UPDATE order_items SET status = 1 '
                'WHERE id = %s AND status = 0',
                (orderItemID,))
    if not cur.rowcount:
        return None
    return orderItemID

# Marks a given order from a given restaurant from in progress to complete
def MarkItemComplete(cur, restaurantName, orderItemID):
    cur.execute('UPDATE order_items SET status = 2, completion_time = CURRENT_TIMESTAMP '
                'WHERE id = %s AND status = 1',
                (orderItemID,))
    if not cur.rowcount:
        return None
    return orderItemID

# Returns an array of orders from a given restaurant that have not been paid for yet
def getUnpaidOrders(cur, restaurantName):
    cur.execute('SELECT o.id, o.submit_time, t.number FROM orders o, tables t, restaurants r '
                'WHERE o.paid = false AND o.table_id = t.id AND t.restaurant_id = r.id AND r.name = %s '
                'ORDER BY o.submit_time', (restaurantName,))
    orders = [{'id': order[0], 'submit_time': order[1], 'table_number': order[2]} for order in cur.fetchall()]
    return orders

# Check if a given order is incomplete
def checkForIncompleteItem(cur, orderID):
    cur.execute('SELECT oi.id FROM order_items oi '
                'WHERE oi.order_id = %s AND (oi.status = 0 OR oi.status = 1) ', (orderID,))
    if not cur.rowcount:
        return False
    else:
        return True

# Return an array of all items within a given incomplete order
def getIncompleteItemsOrder(cur, orderID):
    cur.execute('SELECT oi.id, i.name, oi.status, oi.quantity FROM order_items oi, items i '
                'WHERE oi.order_id = %s AND (oi.status = 0 OR oi.status = 1) AND oi.item_id = i.id ORDER BY oi.id', (orderID,))
    items = [{'id': item[0], 'name': item[1], 'in_progress': item[2] , 'quantity': item[3]} for item in cur.fetchall()]
    return items
