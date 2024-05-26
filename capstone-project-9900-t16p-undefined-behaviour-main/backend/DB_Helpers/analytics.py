from datetime import datetime, timedelta
from dateutil.relativedelta import *

# Obtain and return the sum of all incomes for all orders within a given day, ordered by hour
def hourlyIncome(cur, restaurantName, date):
    date_s = date + ' 00:00:00'
    date_e = date + ' 23:59:59'
    dt_s = datetime.strptime(date_s, "%Y-%m-%d %H:%M:%S")
    dt_e = datetime.strptime(date_e, "%Y-%m-%d %H:%M:%S")

    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]

    incomes = []

    while dt_s < dt_e:
        hourly = dt_s + timedelta(hours=1)
        ts_s = dt_s.strftime("%Y-%m-%d %H:%M:%S")
        ts_hour = hourly.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('SELECT sum(o.total_cost) FROM orders o '
                    'WHERE o.restaurant_id = %s AND o.submit_time >= %s AND o.submit_time < %s',
                    (restaurantID, ts_s, ts_hour) )
        result = cur.fetchone()[0]
        if result:
            incomes.append(float(result))
        else: 
            incomes.append(0)
        dt_s = hourly
    
    return incomes

# Obtain and return the sum of all incomes for all orders within a given week, ordered by day
def dailyIncome(cur, restaurantName, date):
    date_s = date + ' 00:00:00'
    dt_s = datetime.strptime(date_s, "%Y-%m-%d %H:%M:%S")
    dt_e = dt_s + timedelta(days=7)

    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]

    incomes = []

    while dt_s < dt_e:
        daily = dt_s + timedelta(days=1)
        ts_s = dt_s.strftime("%Y-%m-%d %H:%M:%S")
        ts_day = daily.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('SELECT sum(o.total_cost) FROM orders o '
                    'WHERE o.restaurant_id = %s AND o.submit_time >= %s AND o.submit_time < %s',
                    (restaurantID, ts_s, ts_day) )
        result = cur.fetchone()[0]
        if result:
            incomes.append(float(result))
        else: 
            incomes.append(0)
        dt_s = daily
    
    return incomes

# Obtain and return the sum of all incomes for all orders within a given year, ordered by month
def monthlyIncome(cur, restaurantName, year):
    date_s = year + '-01-01 00:00:00'
    date_e = year + '-12-31 00:00:00'
    dt_s = datetime.strptime(date_s, "%Y-%m-%d %H:%M:%S")
    dt_e = datetime.strptime(date_e, "%Y-%m-%d %H:%M:%S")

    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]

    incomes = []

    while dt_s < dt_e:
        monthly = dt_s + relativedelta(months=+1)
        ts_s = dt_s.strftime("%Y-%m-%d %H:%M:%S")
        ts_day = monthly.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('SELECT sum(o.total_cost) FROM orders o '
                    'WHERE o.restaurant_id = %s AND o.submit_time >= %s AND o.submit_time < %s',
                    (restaurantID, ts_s, ts_day) )
        result = cur.fetchone()[0]
        if result:
            incomes.append(float(result))
        else: 
            incomes.append(0)
        dt_s = monthly
    
    return incomes

# Obtain and return the count of orders within a given day, ordered by hour
def customerFrequencyHourly(cur, restaurantName, date):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]

    # Extract the start and end of analysis period
    dateTimeString = date + ' 00:00:00'
    dateTime = datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S")
    endTime = dateTime + timedelta(hours = 24)

    attendanceRates = []
    while dateTime < endTime:
        start = dateTime.strftime("%Y-%m-%d %H:%M:%S")
        dateTime = dateTime + timedelta(hours=1)
        end = dateTime.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('SELECT count(*) FROM orders WHERE submit_time >= %s AND submit_time < %s AND restaurant_id = %s', (start, end, restaurantID))
        attendanceRates.append(cur.fetchone()[0])
    return attendanceRates

# Obtain and return the count of orders within a given week, ordered by day
def customerFrequencyDaily(cur, restaurantName, date):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]

    # Extract the start and end of analysis period
    dateTimeString = date + ' 00:00:00'
    dateTime = datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S")
    endTime = dateTime + timedelta(days=7)

    attendanceRates = []
    while dateTime < endTime:
        start = dateTime.strftime("%Y-%m-%d %H:%M:%S")
        dateTime = dateTime + timedelta(days=1)
        end = dateTime.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('SELECT count(*) FROM orders WHERE submit_time >= %s AND submit_time < %s AND restaurant_id = %s', (start, end, restaurantID))
        attendanceRates.append(cur.fetchone()[0])
    return attendanceRates

# Obtain and return the count of orders within a given year, ordered by month
def customerFrequencyMonthly(cur, restaurantName, year):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]

    # Extract the start and end of analysis period
    dateTimeString = year + '-01-01 00:00:00'
    dateTime = datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S")
    endTime = dateTime + relativedelta(years=+1)

    attendanceRates = []
    while dateTime < endTime:
        start = dateTime.strftime("%Y-%m-%d %H:%M:%S")
        dateTime = dateTime + relativedelta(months=+1)
        end = dateTime.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute('SELECT count(*) FROM orders WHERE submit_time >= %s AND submit_time < %s AND restaurant_id = %s', (start, end, restaurantID))
        attendanceRates.append(cur.fetchone()[0])
    return attendanceRates

# Return mean, median, minimum, and maximum order count for all orders within a given day
def orderCostDay(cur, restaurantName, date):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]

    # Extract the start and end of analysis period
    dateTimeString = date + ' 00:00:00'
    startTime = datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S")
    start = startTime.strftime("%Y-%m-%d %H:%M:%S")
    endTime = startTime + timedelta(days=1)
    end = endTime.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute('SELECT avg(total_cost), min(total_cost), max(total_cost) FROM orders WHERE restaurant_id = %s '
                'AND submit_time >= %s AND submit_time < %s', (restaurantID, start, end))
    result = cur.fetchone()
    if not result[0]:
        return {'mean':0, 'min':0, 'max':0, 'median':0}
    orderCostSummary = {'mean':float(result[0]), 'min':float(result[1]), 'max':float(result[2])}
    cur.execute('SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_cost) FROM orders WHERE restaurant_id = %s '
                'AND submit_time >= %s AND submit_time < %s', (restaurantID, start, end))
    result = cur.fetchone()
    orderCostSummary['median'] = result[0]
    return orderCostSummary

# Return mean, median, minimum, and maximum order count for all orders within a given week
def orderCostWeek(cur, restaurantName, date):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]

    # Extract the start and end of analysis period
    dateTimeString = date + ' 00:00:00'
    startTime = datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S")
    start = startTime.strftime("%Y-%m-%d %H:%M:%S")
    endTime = startTime + timedelta(days=7)
    end = endTime.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute('SELECT avg(total_cost), min(total_cost), max(total_cost) FROM orders WHERE restaurant_id = %s '
                'AND submit_time >= %s AND submit_time < %s', (restaurantID, start, end))
    result = cur.fetchone()
    if not result[0]:
        return {'mean':0, 'min':0, 'max':0, 'median':0}
    orderCostSummary = {'mean':float(result[0]), 'min':float(result[1]), 'max':float(result[2])}
    cur.execute('SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_cost) FROM orders WHERE restaurant_id = %s '
                'AND submit_time >= %s AND submit_time < %s', (restaurantID, start, end))
    result = cur.fetchone()
    orderCostSummary['median'] = result[0]
    return orderCostSummary

# Return mean, median, minimum, and maximum order count for all orders within a given month
def orderCostMonth(cur, restaurantName, month):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]

    # Extract the start and end of analysis period
    dateTimeString = month + '-01 00:00:00'
    startTime = datetime.strptime(dateTimeString, "%Y-%m-%d %H:%M:%S")
    start = startTime.strftime("%Y-%m-%d %H:%M:%S")
    endTime = startTime + relativedelta(months=+1)
    end = endTime.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute('SELECT avg(total_cost), min(total_cost), max(total_cost) FROM orders WHERE restaurant_id = %s '
                'AND submit_time >= %s AND submit_time < %s', (restaurantID, start, end))
    result = cur.fetchone()
    if not result[0]:
        return {'mean':0, 'min':0, 'max':0, 'median':0}
    orderCostSummary = {'mean':float(result[0]), 'min':float(result[1]), 'max':float(result[2])}
    cur.execute('SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_cost) FROM orders WHERE restaurant_id = %s '
                'AND submit_time >= %s AND submit_time < %s', (restaurantID, start, end))
    result = cur.fetchone()
    orderCostSummary['median'] = result[0]
    return orderCostSummary

# Return an array of all items offered by a given restaurant in order of order count
def ItemPopularity(cur, restaurantName):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]
    cur.execute('SELECT i.name, sum(oi.quantity) AS count FROM items i, order_items oi, orders o '
                'WHERE i.id = oi.item_id AND o.id = oi.order_id AND o.restaurant_id = %s GROUP BY i.name ORDER BY count',
                (restaurantID,))

    items = cur.fetchall()
    return items

# Return an array of all items offered by a given restaurant in order of the average difference between submission time and delivery time
def ItemSpeed(cur, restaurantName):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    result = cur.fetchone()
    if not result:
        return None
    restaurantID = result[0]
    cur.execute('SELECT i.name, sum(quantity*(oi.delivery_time - o.submit_time))/sum(oi.quantity) '
                'AS avg FROM items i, order_items oi, orders o WHERE i.id = oi.item_id AND oi.order_id = o.id AND o.restaurant_id = %s '
                'AND oi.delivery_time IS NOT NULL GROUP BY i.name ORDER BY avg',
                (restaurantID,))
    items = [[item[0], str(item[1])] for item in cur.fetchall()]
    return items

# Return the three most commonly ordered items offered by a given restaurant
def PopularItems(cur, restaurantName):
    cur.execute('SELECT id FROM restaurants WHERE name = %s', (restaurantName,))
    res = cur.fetchone()
    if not res:
        return None
    restaurantID = res[0]

    cur.execute('SELECT oi.item_id FROM order_items oi, orders o '
                'WHERE oi.order_id = o.id AND o.restaurant_id = %s '
                'GROUP BY item_id ' 
                'ORDER BY sum(quantity) DESC LIMIT 3', (restaurantID,))
    result = cur.fetchall()
    items = [item[0] for item in result]
    return items
