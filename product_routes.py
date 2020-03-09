import os
import uuid
from flask import Blueprint
from flask import Flask, json, Response, request, abort
from custom_logger import setup_logger

# Set up the custom logger and the Blueprint
logger = setup_logger(__name__)
product_module = Blueprint('products', __name__)

logger.info("Intialized product routes")

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'products.json')

# load products static db from json file
with open(my_file) as f:
    products = json.load(f)

# Allow the default route to return a health check
@product_module.route('/')
def health_check():
    return "This a health check. Product Management Service is up and running."

@product_module.route('/products')
def get_all_products():
    
    try:
        serviceResponse = json.dumps({'products': products})
    except Exception as e:
        logger.error(e)
        abort(404)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"
    
    return resp
    
@product_module.route("/products/<string:product_id>", methods=['GET'])
def get_product(product_id):
    
    product = [p for p in products if p['product_id'] == product_id]

    try:
        serviceResponse = json.dumps({'products': product[0]})
    except Exception as e:
        logger.error(e)
        abort(404)

    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.route("/products", methods=['POST'])
def create_product():

    try:
        product_dict = json.loads(request.data)

        product = {
            'product_id': str(uuid.uuid4()),
            'name': product_dict['name'],
            'description': product_dict['description'],
            'image_url': product_dict['image_url']
        }

        products.append(product)

        serviceResponse = json.dumps({
                'products': product,
                'status': 'CREATED OK'
                })

        resp = Response(serviceResponse, status=201)

    except Exception as e:
        logger.error(e)
        abort(400)
   
    resp.headers["Content-Type"] = "application/json"

    return resp


@product_module.route("/products/<product_id>", methods=['PUT'])
def update_product(product_id):
    
    try:
        #creates a new product. The product id is automatically generated.
        product_dict = json.loads(request.data)
        
        product = [p for p in products if p['product_id'] == product_id]

        product[0]['name'] = request.json.get('name', product[0]['name'])
        product[0]['description'] = request.json.get('description', product[0]['description'])
        product[0]['image_url'] = request.json.get('image_url', product[0]['image_url'])
        
        product = {
            'name': request.json.get('name', product[0]['name']), 
            'description' : request.json.get('description', product[0]['description']),
            'image_url' : request.json.get('image_url', product[0]['image_url'])
        }

        serviceResponse = json.dumps({
                'products': product,
                'status': 'UPDATED OK'
                })

    except Exception as e:
        logger.error(e)
        abort(404)
   
    resp = Response(serviceResponse, status=200)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.route("/products/<product_id>", methods=['DELETE'])
def delete_product(product_id):
    try:
        product = [p for p in products if p['product_id'] == product_id]

        #deletes a product given its id.
        serviceResponse = json.dumps({
                'products' : product,
                'status': 'DELETED OK'
            })

        products.remove(product[0])

    except Exception as e:
        logger.error(e)
        abort(400)
   
    resp = Response(serviceResponse)
    resp.headers["Content-Type"] = "application/json"

    return resp

@product_module.errorhandler(404)
def item_not_found(e):
    # note that we set the 404 status explicitly
    return json.dumps({'error': 'Product not found'}), 404

@product_module.errorhandler(400)
def bad_request(e):
    # note that we set the 400 status explicitly
    return json.dumps({'error': 'Bad request'}), 400
