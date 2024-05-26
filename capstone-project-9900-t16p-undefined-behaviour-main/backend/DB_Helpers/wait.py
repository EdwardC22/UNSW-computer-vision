# Return an array of items from all orders within a given restaurant that are completed but not delivered
def getCompletedItems(cur, restaurantName):
    cur.execute('SELECT oi.id, i.name, oi.quantity, t.number FROM order_items oi, items i, orders o, tables t, restaurants r WHERE '
                'oi.status = 2 AND oi.item_id = i.id AND oi.order_id = o.id AND o.table_id = t.id AND t.restaurant_id = r.id AND r.name = %s '
                'ORDER BY oi.completion_time', (restaurantName,))
    items = [{'id': item[0], 'name': item[1], 'quantity': item[2], 'table_number': item[3]} for item in cur.fetchall()]
    return items

# Mark a given item within an order as delivered
def deliverCompletedItem(cur, orderItemID):
    cur.execute('UPDATE order_items SET status = 3, delivery_time = CURRENT_TIMESTAMP WHERE id = %s AND status = 2', (orderItemID,))
    if not cur.rowcount:
        return None
    return orderItemID

# Return an array of all tables within a given restaurant that are requesting assistance currently
def getAssistance(cur, restaurantName):
    cur.execute('SELECT a.id, t.number, a.bill FROM assistance a, tables t, restaurants r WHERE '
                'a.complete = false AND a.table_id = t.id AND t.restaurant_id = r.id AND r.name = %s ORDER BY a.submit_time',
                (restaurantName,))
    assistances = [{'id': assist[0], 'table_number': assist[1], 'bill': assist[2]} for assist in cur.fetchall()]
    return assistances

# Mark a given table's assistance request as completed
def completeAssistance(cur, assistanceID):
    cur.execute('UPDATE assistance SET complete = true WHERE id = %s', (assistanceID,))
    if not cur.rowcount:
        return None
    return assistanceID
