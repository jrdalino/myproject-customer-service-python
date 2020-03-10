import os
import uuid
from flask import Blueprint
from flask import Flask, json, Response, request, abort
from custom_logger import setup_logger
import customer_table_client

# Set up the custom logger and the Blueprint
logger = setup_logger(__name__)
customer_module = Blueprint('customers', __name__)

logger.info("Intialized customer routes")

# Load customers static db from json file
THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
my_file = os.path.join(THIS_FOLDER, "tests", 'customers.json')

with open(my_file) as f:
    customers = json.load(f)

# Allow the default route to return a health check
@customer_module.route('/')
def health_check():
    return "This a health check. Customer Management Service is up and running."

# Get all customers
@customer_module.route('/customers')
def get_all_customers():
    
    try:
        #serviceResponse = json.dumps({'customers': customers}) # static database
        serviceResponse = customer_table_client.get_all_customers_ddb() # dynamodb
    except Exception as e:
        logger.error(e)
        abort(404)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"
    
    return resp

# Get customer by customer_id
@customer_module.route("/customers/<string:customer_id>", methods=['GET'])
def get_customer(customer_id):
    
    customer = [p for p in customers if p['customer_id'] == customer_id]

    try:
        serviceResponse = json.dumps({'customers': customer[0]})
    except Exception as e:
        logger.error(e)
        abort(404)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

# Add a new customer
@customer_module.route("/customers", methods=['POST'])
def create_customer():

    try:
        customer_dict = json.loads(request.data)

        customer = {
            'customer_id': str(uuid.uuid4()),
            'first_name': customer_dict['first_name'],
            'last_name': customer_dict['last_name'],
            'email': customer_dict['email'],
            'dob': customer_dict['dob'],
            'gender': customer_dict['gender']
        }

        customers.append(customer)

        serviceResponse = json.dumps({
                'customers': customer,
                'status': 'CREATED OK'
                })

        resp = Response(serviceResponse, status=201)

    except Exception as e:
        logger.error(e)
        abort(400)
   
    resp.headers["Content-Type"] = "application/json"

    return resp

# Update customer by customer_id
@customer_module.route("/customers/<customer_id>", methods=['PUT'])
def update_customer(customer_id):
    
    try:
        #creates a new customer. The customer id is automatically generated.
        customer_dict = json.loads(request.data)
        
        customer = [p for p in customers if p['customer_id'] == customer_id]

        customer[0]['first_name'] = request.json.get('first_name', customer[0]['first_name'])
        customer[0]['last_name'] = request.json.get('last_name', customer[0]['last_name'])
        customer[0]['email'] = request.json.get('email', customer[0]['email'])
        customer[0]['dob'] = request.json.get('dob', customer[0]['dob'])
        customer[0]['gender'] = request.json.get('gender', customer[0]['gender'])
        
        customer = {
            'first_name' : request.json.get('first_name', customer[0]['first_name']),
            'last_name' : request.json.get('last_name', customer[0]['last_name']),
            'email' : request.json.get('email', customer[0]['email']),
            'dob' : request.json.get('dob', customer[0]['dob']),
            'gender' : request.json.get('gender', customer[0]['gender'])
        }

        serviceResponse = json.dumps({
                'customers': customer,
                'status': 'UPDATED OK'
                })

    except Exception as e:
        logger.error(e)
        abort(404)
   
    resp = Response(serviceResponse, status=200)
    resp.headers["Content-Type"] = "application/json"

    return resp

# Delete customer by customer_id
@customer_module.route("/customers/<customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    try:
        customer = [p for p in customers if p['customer_id'] == customer_id]

        serviceResponse = json.dumps({
                'customers' : customer,
                'status': 'DELETED OK'
            })

        customers.remove(customer[0])

    except Exception as e:
        logger.error(e)
        abort(400)
   
    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

@customer_module.errorhandler(404)
def item_not_found(e):
    # note that we set the 404 status explicitly
    return json.dumps({'error': 'Customer not found'}), 404

@customer_module.errorhandler(400)
def bad_request(e):
    # note that we set the 400 status explicitly
    return json.dumps({'error': 'Bad request'}), 400