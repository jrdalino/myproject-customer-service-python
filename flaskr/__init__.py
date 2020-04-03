#!/usr/bin/env python
import os

from flask import Flask
from flask_cors import CORS

# Add new blueprints here
if __package__ is None or __package__ == '':
    # uses current directory visibility
		from customer_routes import customer_module
else:
    # uses current package visibility
    from flaskr.customer_routes import customer_module

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	CORS(app)
	app.config.from_mapping(
		SECRET_KEY="dev",
		DATABASE="sample://db-string"
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile("config.py", silent=True)
	else:
		# load the test config if passed in
		app.config.update(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# Add a blueprint for the customers module
	app.register_blueprint(customer_module)
	
	return app