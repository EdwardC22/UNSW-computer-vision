# Import relevant packages
import json, psycopg2, re, config
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity, JWTManager, set_access_cookies, unset_jwt_cookies

# Import from helper files
from DB_Helpers.login import *
from DB_Helpers.menu import *
from DB_Helpers.order import *
from DB_Helpers.kitchen import *
from DB_Helpers.wait import *
from DB_Helpers.analytics import *

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='orderup',
                            user = config.DB_USERNAME,
                            password = config.DB_PASSWORD)
    return conn

def make_error(error_msg):
    return jsonify({
                       "error": error_msg
                   })

# Refresh any token that is within 30 minutes of expiring
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

# Page where a new restaurant can be registered
@app.route('/register/', methods=['POST'])
def registration():
    conn = get_db_connection()
    cur = conn.cursor()
    credentials = json.loads(request.data)
    username = credentials.get('username')
    email = credentials.get('email')
    password = credentials.get('password')
    restaurantName = credentials.get('restaurant_name')
    # Check none of the values are empty
    if not (username and email and password and restaurantName): #eval if any of inner condition is false 
        return make_error('Username, email password or restaurant name left empty'), 400
    # Check username is valid
    if not re.search('^[a-zA-Z0-9_]+$', username):
        return make_error('Invalid username'), 400
    # Check email is valid
    if not re.search('^[\w\.=-]+@[\w\.-]+\.[\w]{2,3}$', email):
        return make_error('Invalid email'), 400
    # Check restaurant name is valid
    if not re.search('^[a-zA-Z ]+$', restaurantName):
        return make_error('Invalid restaurant name'), 400
    # Check username is unique
    if getUser(cur, username, None):
        return make_error('Username {} already exists'.format(username)), 400
    # Check email is unique
    if getUser(cur, None, email):
        return make_error('Email {} already in use'.format(email)), 400
    # Replace spaces with underscores in restaurant name
    restaurantName = restaurantName.replace(" ", "_")
    credentials['restaurant_name'] = restaurantName
    # Check restaurant is unique
    if getRestaurant(cur, restaurantName):
        return make_error('Restaurant {} already exists'.format(restaurantName)), 400
    # Add user
    managerID = addUser(cur, credentials)
    if not managerID:
        return make_error('Error on user registration'), 500
    conn.commit()
    cur.close()
    conn.close()
    response = jsonify({'status': 'success'})
    accessToken = create_access_token(identity=managerID)
    set_access_cookies(response, accessToken)
    return response

# Login page for a staff member
@app.route('/<string:restaurantName>/login/', methods=['POST'])
def login(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    credentials = json.loads(request.data)
    username = credentials.get('username')
    password = credentials.get('password')
    manager = getUser(cur, username, None)
    if not manager:
        return make_error('Username {} does not exist'.format(username)), 400
    if not verifyManagerRestaurant(cur, manager.get('id'), restaurantName):
        return make_error('Username {} is not the manager of {}'.format(username, restaurantName)), 400
    if not verifyPassword(cur, username, password):
        return make_error('Incorrect password'), 400
    response = jsonify({'status': 'success'})
    accessToken = create_access_token(identity=manager.get('id'))
    set_access_cookies(response, accessToken)
    return response

# Verify a manager is logged in to a restaurant
@app.route('/<string:restaurantName>/verifytoken/', methods=['POST'])
@jwt_required()
def verifyToken(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    return jsonify({'status': 'success'})

# Logout
@app.route("/logout/", methods=["POST"])
def logout():
    response = jsonify({'status': 'success'})
    unset_jwt_cookies(response)
    return response

# Menu display
@app.route('/<string:restaurantName>/')
def index(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    categories = getCategoriesRestaurant(cur, restaurantName)
    popularItems = PopularItems(cur, restaurantName)
    for category in categories:
        items = getItemsCategory(cur, category['id'], popularItems)
        category['items'] = items
    cur.close()
    conn.close()
    return jsonify(categories)

# Table number display and update
@app.route('/<string:restaurantName>/tables/', methods=['GET', 'POST'])
@jwt_required(optional=True)
def tableNumbers(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        # Verify user identity
        managerID = get_jwt_identity()
        if not managerID or not verifyManagerRestaurant(cur, managerID, restaurantName):
            return make_error('User is not the manager of {}'.format(restaurantName)), 400
        tables = updateTables(cur, restaurantName, json.loads(request.data))
        if not tables:
            return make_error("Could not update table number"), 400
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'tables': tables})
    tables = getTables(cur, restaurantName)
    cur.close()
    conn.close()
    return jsonify({'tables': tables})

# Create a category
@app.route('/<string:restaurantName>/createcategory/', methods=['POST'])
@jwt_required()
def createCategory(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    categoryID = addCategory(cur, restaurantName, json.loads(request.data))
    if not categoryID:
        cur.close()
        conn.close()
        return make_error("Could not add category"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'categoryID': categoryID})

# Create an item in a category
@app.route('/<string:restaurantName>/createitem/', methods=['POST'])
@jwt_required()
def createItem(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    itemID = addItem(cur, json.loads(request.data))
    if not itemID:
        cur.close()
        conn.close()
        return make_error("Could not add item"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'itemID': itemID})

# Edit a category
@app.route('/<string:restaurantName>/editcategory/<int:categoryID>/', methods=['PUT'])
@jwt_required()
def editCategory(restaurantName, categoryID):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    if not updateCategory(cur, categoryID, json.loads(request.data)):
        cur.close()
        conn.close()
        return make_error("Could not edit category"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'categoryID': categoryID})

# Change the position of a category
@app.route('/<string:restaurantName>/editcategorypos/<int:categoryID>/', methods=['PUT'])
@jwt_required()
def editCategoryPos(restaurantName, categoryID):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    if not updateCategoryPos(cur, categoryID, json.loads(request.data)):
        cur.close()
        conn.close()
        return make_error("Could not change the position of category"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'categoryID': categoryID})

# Edit an item
@app.route('/<string:restaurantName>/edititem/<int:itemID>/', methods=['PUT'])
@jwt_required()
def editItem(restaurantName, itemID):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    if not updateItem(cur, itemID, json.loads(request.data)):
        cur.close()
        conn.close()
        return make_error("Could not edit item"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'itemID': itemID})

# Change the position of an item
@app.route('/<string:restaurantName>/edititempos/<int:itemID>/', methods=['PUT'])
@jwt_required()
def editItemPos(restaurantName, itemID):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    if not updateItemPos(cur, itemID, json.loads(request.data)):
        cur.close()
        conn.close()
        return make_error("Could not change the position of item"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'itemID': itemID})

# Change the category of an item
@app.route('/<string:restaurantName>/edititemcat/<int:itemID>/', methods=['PUT'])
@jwt_required()
def editItemCategory(restaurantName, itemID):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    if not updateItemCategory(cur, itemID, json.loads(request.data)):
        cur.close()
        conn.close()
        return make_error("Could not change the category of item"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'itemID': itemID})

# Delete a category and its items
@app.route('/<string:restaurantName>/deletecategory/<int:categoryID>/', methods=['DELETE'])
@jwt_required()
def deleteCategory(restaurantName, categoryID):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    if not removeCategory(cur, categoryID):
        cur.close()
        conn.close()
        return make_error("Could not delete category"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

# Delete an item
@app.route('/<string:restaurantName>/deleteitem/<int:itemID>/', methods=['DELETE'])
@jwt_required()
def deleteItem(restaurantName, itemID):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    if not removeItem(cur, itemID):
        cur.close()
        conn.close()
        return make_error("Could not delete item"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

# Obtain or submit an order
@app.route('/<string:restaurantName>/<int:tableNumber>/', methods=['GET', 'POST'])
def order(restaurantName, tableNumber):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        if not addOrder(cur, restaurantName, tableNumber, json.loads(request.data)):
            cur.close()
            conn.close()
            return make_error("Could not submit order"), 400
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'status': 'success'})
    orders = getOrder(cur, restaurantName, tableNumber)
    cur.close()
    conn.close()
    return jsonify({'order': orders})

# Get orders received or in progress orders
@app.route('/<string:restaurantName>/orders/')
def displayIncompleteOrders(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    orders = getUnpaidOrders(cur, restaurantName)
    validOrders = []

    for order in orders:
        if checkForIncompleteItem(cur, order['id']):
            validOrders.append(order)

    for validOrder in validOrders:
        items = getIncompleteItemsOrder(cur, validOrder['id'])
        validOrder['items'] = items

    cur.close()
    conn.close()
    return jsonify({'orders': validOrders})

# Get items to be delivered
@app.route('/<string:restaurantName>/completeitems/')
def displayCompleteItems(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    items = getCompletedItems(cur, restaurantName)
    cur.close()
    conn.close()
    return jsonify({'complete_items': items})
    
# Mark an item in order as in progress
@app.route('/<string:restaurantName>/ordereditems/<int:orderItemID>/', methods=['PUT'])
def itemInProgress(restaurantName, orderItemID):
    conn = get_db_connection()
    cur = conn.cursor()
    if not MarkItemInprogress(cur, restaurantName, orderItemID):
        cur.close()
        conn.close()
        return make_error("Could not mark item as in progress"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

# Mark an item in order as complete
@app.route('/<string:restaurantName>/inprogessitems/<int:orderItemID>/', methods=['PUT'])
def itemComplete(restaurantName, orderItemID):
    conn = get_db_connection()
    cur = conn.cursor()
    if not MarkItemComplete(cur, restaurantName, orderItemID):
        cur.close()
        conn.close()
        return make_error("Could not mark item as completed"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

# Mark an item delivered
@app.route('/<string:restaurantName>/completeitems/<int:orderItemID>/', methods=['PUT'])
def itemDelivered(restaurantName, orderItemID):
    conn = get_db_connection()
    cur = conn.cursor()
    if not deliverCompletedItem(cur, orderItemID):
        cur.close()
        conn.close()
        return make_error("Could not mark item as delivered"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

# Request bill or assistance
@app.route('/<string:restaurantName>/<int:tableNumber>/assistance/', methods=['POST'])
def requestAssistance(restaurantName, tableNumber):
    conn = get_db_connection()
    cur = conn.cursor()
    if not addAssistance(cur, restaurantName, tableNumber, json.loads(request.data)):
        cur.close()
        conn.close()
        return make_error("Could not request assistance"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

# Get assistance requests
@app.route('/<string:restaurantName>/assistance/')
def displayAssistance(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    assistance = getAssistance(cur, restaurantName)
    cur.close()
    conn.close()
    return jsonify({'assistance': assistance})

# Mark an assistance request as complete
@app.route('/<string:restaurantName>/assistance/<int:assistanceID>/', methods=['PUT'])
def editAssistance(restaurantName, assistanceID):
    conn = get_db_connection()
    cur = conn.cursor()
    if not completeAssistance(cur, assistanceID):
        return make_error("Could not mark assistance request as complete"), 400
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

# Get hourly income for selected date
@app.route('/<string:restaurantName>/analysis/hourlyincome/<string:date>/')
@jwt_required()
def getHourlyIncome(restaurantName, date):
    
    # the date format will be like '2022-11-03'
    
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    income = hourlyIncome(cur, restaurantName, date)
    if not income:
        cur.close()
        conn.close()
        return make_error("Could not get the income"), 400
    cur.close()
    conn.close()
    return jsonify({'hourly_income': income})

# Get daily income for the week starting from selected date
@app.route('/<string:restaurantName>/analysis/dailyincome/<string:date>/')
@jwt_required()
def getDailyIncome(restaurantName, date):
    
    # the date format will be like '2022-11-03'
    
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    income = dailyIncome(cur, restaurantName, date)
    if not income:
        cur.close()
        conn.close()
        return make_error("Could not get the income"), 400
    cur.close()
    conn.close()
    return jsonify({'daily_income': income})

# Get monthly income for selected year
@app.route('/<string:restaurantName>/analysis/monthlyincome/<string:year>/')
@jwt_required()
def getMonthlyIncome(restaurantName, year):
    
    # the year format will be like '2022'
    
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    income = monthlyIncome(cur, restaurantName, year)
    if not income:
        cur.close()
        conn.close()
        return make_error("Could not get the income"), 400
    cur.close()
    conn.close()
    return jsonify({'monthly_income': income})

# Get hourly customer frequency for selected date 
@app.route('/<string:restaurantName>/analysis/hourlycustomerfrequency/<string:date>/')
@jwt_required()
def getHourlyCustomerFrequency(restaurantName, date):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    frequency = customerFrequencyHourly(cur, restaurantName, date)
    if not frequency:
        cur.close()
        conn.close()
        return make_error("Could not get hourly customer frequency"), 400
    cur.close()
    conn.close()
    return jsonify({'hourly_customer_frequency': frequency})

# Get daily customer frequency for week starting from selected date
@app.route('/<string:restaurantName>/analysis/dailycustomerfrequency/<string:date>/')
@jwt_required()
def getDailyCustomerFrequency(restaurantName, date):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    frequency = customerFrequencyDaily(cur, restaurantName, date)
    if not frequency:
        cur.close()
        conn.close()
        return make_error("Could not get daily customer frequency"), 400
    cur.close()
    conn.close()
    return jsonify({'daily_customer_frequency': frequency})

# Get monthly customer frequency for selected year
@app.route('/<string:restaurantName>/analysis/monthlycustomerfrequency/<string:year>/')
@jwt_required()
def getMonthlyCustomerFrequency(restaurantName, year):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    frequency = customerFrequencyMonthly(cur, restaurantName, year)
    if not frequency:
        cur.close()
        conn.close()
        return make_error("Could not get monthly customer frequency"), 400
    cur.close()
    conn.close()
    return jsonify({'monthly_customer_frequency': frequency})

# Get the mean, median, maximum and minimumn cost of orders for selected date
@app.route('/<string:restaurantName>/analysis/dailyorderstats/<string:date>/')
@jwt_required()
def getDailyOrderStats(restaurantName, date):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    orderStats = orderCostDay(cur, restaurantName, date)
    if not orderStats:
        cur.close()
        conn.close()
        return make_error("Could not get order statistics"), 400
    cur.close()
    conn.close()
    return jsonify(orderStats)

# Get the mean, median, maximum and minimumn cost of orders for week starting from selected date
@app.route('/<string:restaurantName>/analysis/weeklyorderstats/<string:date>/')
@jwt_required()
def getWeeklyOrderStats(restaurantName, date):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    orderStats = orderCostWeek(cur, restaurantName, date)
    if not orderStats:
        cur.close()
        conn.close()
        return make_error("Could not get order statistics"), 400
    cur.close()
    conn.close()
    return jsonify(orderStats)

# Find most and least popular items
@app.route('/<string:restaurantName>/analysis/itempopularity/', methods = ['GET'])
@jwt_required()
def getItemPopularity(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    items = ItemPopularity(cur, restaurantName)
    if not items:
            cur.close()
            conn.close()
            return make_error("Could not get items"), 400
    cur.close()
    conn.close()
    return jsonify({'items': items})

# Find fastest and slowest delivered items
@app.route('/<string:restaurantName>/analysis/itemspeed/', methods = ['GET'])
@jwt_required()
def getItemSpeed(restaurantName):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    items = ItemSpeed(cur, restaurantName)
    if not items:
            cur.close()
            conn.close()
            return make_error("Could not get items"), 400
    cur.close()
    conn.close()
    return jsonify({'items': items})

# Get the mean, median, maximum and minimumn cost of orders for month of the selected date
@app.route('/<string:restaurantName>/analysis/monthlyorderstats/<string:month>/')
@jwt_required()
def getMonthlyOrderStats(restaurantName, month):
    conn = get_db_connection()
    cur = conn.cursor()
    # Verify user identity
    managerID = get_jwt_identity()
    if not verifyManagerRestaurant(cur, managerID, restaurantName):
        return make_error('User is not the manager of {}'.format(restaurantName)), 400
    orderStats = orderCostMonth(cur, restaurantName, month)
    if not orderStats:
        cur.close()
        conn.close()
        return make_error("Could not get order statistics"), 400
    cur.close()
    conn.close()
    return jsonify(orderStats)
