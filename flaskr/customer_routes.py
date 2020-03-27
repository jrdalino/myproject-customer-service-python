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
        # serviceResponse = json.dumps({'customers': customers})
        # note: uncomment this to use dynamodb
        serviceResponse = customer_table_client.getAllCustomers()
    except Exception as e:
        logger.error(e)
        abort(400)
    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"
    return resp

# Get customer by customerId
@customer_module.route("/customers/<string:customerId>", methods=['GET'])
def get_customer(customerId):
    try:
        # note: uncomment this to use static db
        # customer = [c for c in customers if c['customerId'] == customerId]
        # serviceResponse = json.dumps({'customers': {
        #         'data': customer[0],
        #         'status': 'GET OK'
        #         }
        #     })
        # note: uncomment this to use dynamodb
        serviceResponse = customer_table_client.getCustomer(customerId) 
    except Exception as e:
        logger.error(e)
        abort(400)
    resp = Response(serviceResponse, 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

# Add a new customer
@customer_module.route("/customers", methods=['POST'])
def create_customer():
    try:
        customerDict = json.loads(request.data)
        # note: uncomment this to use static db
        # customer = {
        #     'customerId': str(uuid.uuid4()),
        #     'firstName': customerDict['firstName'],
        #     'lastName': customerDict['lastName'],
        #     'email': customerDict['email'],
        #     'userName': customerDict['userName'],        
        #     'birthDate': customerDict['birthDate'],
        #     'gender': customerDict['gender'],
        #     'custNumber': customerDict['custNumber'],
        #     'cardNumber': customerDict['cardNumber'],
        #     'phoneNumber': customerDict['phoneNumber'],
        #     'createdDate': customerDict['createdDate'],
        #     'updatedDate': customerDict['updatedDate'],
        #     'profilePhotoUrl': customerDict['profilePhotoUrl']
        # }
        # customers.append(customer)
        # serviceResponse = json.dumps({
        #         'customers': {
        #             'data': customer,
        #             'status': 'CREATED OK'
        #             }
        #         })
        # note: uncomment this to use dynamodb
        serviceResponse = customer_table_client.createCustomer(customerDict)
    except Exception as e:
        logger.error(e)
        abort(400)        
    resp = Response(serviceResponse, 201)   
    resp.headers["Content-Type"] = "application/json"
    return resp

# Update customer by customerId
@customer_module.route("/customers/<customerId>", methods=['PUT'])
def update_customer(customerId):
    try:
        customerDict = json.loads(request.data)
        # note: uncomment this to use static db      
        # customer = [c for c in customers if c['customerId'] == customerId]
        # customer[0]['firstName'] = request.json.get('firstName', customer[0]['firstName'])
        # customer[0]['lastName'] = request.json.get('lastName', customer[0]['lastName'])
        # customer[0]['email'] = request.json.get('email', customer[0]['email'])
        # customer[0]['userName'] = request.json.get('userName', customer[0]['userName'])        
        # customer[0]['birthDate'] = request.json.get('birthDate', customer[0]['birthDate'])
        # customer[0]['gender'] = request.json.get('gender', customer[0]['gender'])
        # customer[0]['custNumber'] = request.json.get('custNumber', customer[0]['custNumber'])
        # customer[0]['cardNumber'] = request.json.get('cardNumber', customer[0]['cardNumber'])
        # customer[0]['phoneNumber'] = request.json.get('phoneNumber', customer[0]['phoneNumber'])
        # customer[0]['createdDate'] = request.json.get('createdDate', customer[0]['createdDate'])
        # customer[0]['updatedDate'] = request.json.get('updatedDate', customer[0]['updatedDate'])
        # customer[0]['profilePhotoUrl'] = request.json.get('profilePhotoUrl', customer[0]['profilePhotoUrl'])     
        # customer = {
        #     'firstName' : request.json.get('firstName', customer[0]['firstName']),
        #     'lastName' : request.json.get('lastName', customer[0]['lastName']),
        #     'email' : request.json.get('email', customer[0]['email']),
        #     'userName' : request.json.get('userName', customer[0]['userName']),        
        #     'birthDate' : request.json.get('birthDate', customer[0]['birthDate']),
        #     'gender' : request.json.get('gender', customer[0]['gender']),
        #     'custNumber' : request.json.get('custNumber', customer[0]['custNumber']),
        #     'cardNumber' : request.json.get('cardNumber', customer[0]['cardNumber']),
        #     'phoneNumber' : request.json.get('phoneNumber', customer[0]['phoneNumber']),
        #     'createdDate' : request.json.get('createdDate', customer[0]['createdDate']),
        #     'profilePhotoUrl' : request.json.get('profilePhotoUrl', customer[0]['profilePhotoUrl'])    
        # }
        # serviceResponse = json.dumps({
        #         'customers': {
        #             'data': customer,
        #             'status': 'UPDATED OK'} 
        #         })
        # note: uncomment this to use dynamodb
        serviceResponse = customer_table_client.updateCustomer(customerId, customerDict)
    except Exception as e:
        logger.error(e)
        abort(400)
    resp = Response(serviceResponse, 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

# Delete customer by customerId
@customer_module.route("/customers/<customerId>", methods=['DELETE'])
def delete_customer(customerId):
    try:
        # note: uncomment this to use static db       
        # customer = [c for c in customers if c['customerId'] == customerId]
        # serviceResponse = json.dumps({
        #         'customers' : {
        #             'data': customer[0],
        #             'status': 'DELETED OK'
        #         }
        #     })
        # customers.remove(customer[0])
        # note: uncomment this to use dynamodb
        serviceResponse = customer_table_client.deleteCustomer(customerId)
    except Exception as e:
        logger.error(e)
        abort(400)
    resp = Response(serviceResponse, 200)
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