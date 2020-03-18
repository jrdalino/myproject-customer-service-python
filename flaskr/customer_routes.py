import os
import uuid
from flask import Blueprint
from flask import Flask, json, Response, request, abort


# Add new blueprints here
if __package__ is None or __package__ == '':
    # uses current directory visibility
    import customer_table_client
    from custom_logger import setup_logger
else:
    # uses current package visibility
    from flaskr import customer_table_client
    from flaskr.custom_logger import setup_logger

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
        # note: uncomment this to use static db
        serviceResponse = json.dumps({'customers': customers})
        # note: uncomment this to use dynamodb
        # serviceResponse = customer_table_client.getAllCustomers()
    except Exception as e:
        logger.error(e)
        abort(404)
    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"
    return resp

# Get customer by customer_id
@customer_module.route("/customers/<string:customer_id>", methods=['GET'])
def get_customer(customer_id):
    try:
        # note: uncomment this to use static db
        customer = [c for c in customers if c['customer_id'] == customer_id]
        serviceResponse = json.dumps({'customers': {
                'data': customer[0]
                }, 
                'status': 'GET OK'
            })
        # note: uncomment this to use dynamodb
        # serviceResponse = customer_table_client.getCustomer(customer_id) 
    except Exception as e:
        logger.error(e)
        abort(404)
    resp = Response(serviceResponse, 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

# Add a new customer
@customer_module.route("/customers", methods=['POST'])
def create_customer():
    try:
        customer_dict = json.loads(request.data)
        # note: uncomment this to use static db

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
                'customers': {
                    'data': customer,
                    'status': 'CREATED OK'
                    }
                })
        # note: uncomment this to use dynamodb
        # serviceResponse = customer_table_client.createCustomer(customer_dict)
    except Exception as e:
        logger.error(e)
        abort(400)        
    resp = Response(serviceResponse, 201)   
    resp.headers["Content-Type"] = "application/json"
    return resp

# Update customer by customer_id
@customer_module.route("/customers/<customer_id>", methods=['PUT'])
def update_customer(customer_id):
    try:
        customer_dict = json.loads(request.data)
        # note: uncomment this to use static db      

        customer = [c for c in customers if c['customer_id'] == customer_id]
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
                'customers': {
                    'data': customer
                },
                'status': 'UPDATED OK'
                })
        # note: uncomment this to use dynamodb
        # serviceResponse = customer_table_client.updateCustomer(customer_id, customer_dict)
    except Exception as e:
        logger.error(e)
        abort(400)

    resp = Response(serviceResponse, 200)
    resp.headers["Content-Type"] = "application/json"
    
    return resp

# Delete customer by customer_id
@customer_module.route("/customers/<customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    try:
        # note: uncomment this to use static db       
        customer = [c for c in customers if c['customer_id'] == customer_id]
        serviceResponse = json.dumps({
                'customers' : {
                    'data': customer[0]
                },
                'status': 'DELETED OK'
            })
        customers.remove(customer[0])
        # note: uncomment this to use dynamodb
        # serviceResponse = customer_table_client.deleteCustomer(customer_id)
    except Exception as e:
        logger.error(e)
        abort(400)
    resp = Response(serviceResponse, 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@customer_module.errorhandler(404)
def item_not_found(e):
    
    # note that we set the 404 status explicitly
    errorResponse = json.dumps({'customers': {
        'data': {},
        'status': 'Customer not found'
        }})

    resp = Response(errorResponse, 404)
    resp.headers["Content-Type"] = "application/json"

    return resp


@customer_module.errorhandler(400)
def bad_request(e):
    # note that we set the 400 status explicitly
    errorResponse = json.dumps({'customers': {
        'data': {},
        'status': 'Bad request'
        }})

    resp = Response(errorResponse, 400)
    resp.headers["Content-Type"] = "application/json"

    return resp