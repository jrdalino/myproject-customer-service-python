#!/usr/bin/env python
from flask import Flask
from flask_cors import CORS

# Add new blueprints here
from customer_routes import customer_module

# Initialize the flask application
app = Flask(__name__)
CORS(app)

# Add a blueprint for the customers module
app.register_blueprint(customer_module)

# Run the application
app.run(host="0.0.0.0", port=5000, debug=True)