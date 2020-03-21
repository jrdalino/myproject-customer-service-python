import boto3
import json
import logging
from collections import defaultdict
import argparse
import uuid

if __package__ is None or __package__ == '':
	# uses current directory visibility
	from custom_logger import setup_logger
	from db import get_db_client
else:
	# uses current package visibility
	from flaskr.custom_logger import setup_logger
	from flaskr.db import get_db_client

logger = setup_logger(__name__)
table_name = 'customers'

def getAllCustomers():
	dynamodb = get_db_client()
	response = dynamodb.scan(
		TableName=table_name
	)
	# logger.info("Logger Response: ")
	# logger.info(response)    
	customer_list = defaultdict(list)
	for item in response["Items"]:
		customer = {
			'customer_id': item["customer_id"]["S"],
			'first_name': item['first_name']['S'],
			'last_name': item['last_name']['S'],
			'email': item['email']['S'],
			'dob': item['dob']['S'],
			'gender': item['gender']['S'],
			'customer_number': item['customer_number']['S'],
			'card_number': item['card_number']['S'],
			'phone': item['phone']['S'],
		}
		customer_list["customers"].append(customer)
	return json.dumps(customer_list)

def getCustomer(customer_id):
	dynamodb = get_db_client()
	response = dynamodb.get_item(
		TableName=table_name,
		Key={
			'customer_id': {
				'S': customer_id
			}
		}
	)
	# logger.info("Logger Response: ")
	# logger.info(response)


	if 'Item' in response:

		item = response['Item']

		customer = {
			'customer_id': item["customer_id"]["S"],
			'first_name': item['first_name']['S'],
			'last_name': item['last_name']['S'],            
			'email': item['email']['S'],
			'dob': item['dob']['S'],
			'gender': item['gender']['S'],
			'customer_number': item['customer_number']['S'],
			'card_number': item['card_number']['S'],
			'phone': item['phone']['S'],
		}

		return json.dumps({'customers': {
			'data' : customer,
			'status': 'GET OK'
			}
		})

	else: 

		return json.dumps({'customers': {
			'data' : {},
			'status': 'Customer not found'
			}
		})




def createCustomer(customer_dict):
	dynamodb = get_db_client()
	customer_id = str(uuid.uuid4())
	first_name = str(customer_dict['first_name'])
	last_name = str(customer_dict['last_name'])
	email = str(customer_dict['email'])
	dob = str(customer_dict['dob'])
	gender = str(customer_dict['gender'])
	customer_number = str(customer_dict['customer_number'])
	card_number = str(customer_dict['card_number'])
	phone = str(customer_dict['phone'])
	response = dynamodb.put_item(
		TableName=table_name,
		Item={
				'customer_id': {
					'S': customer_id
				},
				'first_name': {
					'S' : first_name
				},
				'last_name': {
					'S' : last_name
				},                
				'email' : {
					'S' : email
				},
				'dob': {
					'S' : dob
				},
				'gender': {
					'S' : gender
				},
				'customer_number': {
					'S' : customer_number
				},
				'card_number': {
					'S' : card_number
				},
				'phone': {
					'S' : phone
				}
			}
		)
	# logger.info("Logger Response: ")
	# logger.info(response)
	customer = {
		'data' : {
			'customer_id': customer_id,
			'first_name': first_name,
			'last_name': last_name,        
			'email': email,
			'dob': dob,
			'gender': gender,
			'customer_number': customer_number,
			'card_number': card_number,
			'phone': phone,
		},
		'status' : 'CREATED OK'
	}
	return json.dumps({'customers': customer})

def updateCustomer(customer_id, customer_dict):
	dynamodb = get_db_client()

	first_name = str(customer_dict['first_name'])
	last_name = str(customer_dict['last_name'])
	email = str(customer_dict['email'])
	dob = str(customer_dict['dob'])
	gender = str(customer_dict['gender'])
	customer_number = str(customer_dict['customer_number'])
	card_number = str(customer_dict['card_number'])
	phone = str(customer_dict['phone'])
	response = dynamodb.update_item(
		TableName=table_name,
		Key={
			'customer_id': {
				'S': customer_id
			}
		},
		UpdateExpression="""SET first_name = :p_first_name,
								last_name = :p_last_name,
								email = :p_email,
								dob = :p_dob,
								gender = :p_gender,
								customer_number = :p_customer_number,
								card_number = :p_card_number,
								phone = :p_phone
								""",
		ExpressionAttributeValues={
			':p_first_name': {
				'S' : first_name
			},
			':p_last_name' : {
				'S' : last_name
			},
			':p_email': {
				'S' : email
			},
			':p_dob': {
				'S' : dob
			},
			':p_gender': {
				'S' : gender
			},
			':p_customer_number': {
				'S' : customer_number
			},
			':p_card_number': {
				'S' : card_number
			},
			':p_phone': {
				'S' : phone
			}
		}
	)
	# logger.info("Logger Response: ")
	# logger.info(response)
	customer = {
		'data' : {
			'customer_id': customer_id,
			'first_name': first_name,
			'last_name': last_name,        
			'email': email,
			'dob': dob,
			'gender': gender,
			'customer_number': customer_number,
			'card_number': card_number,
			'phone': phone,
		},
		'status' : 'UPDATED OK'
	}
	return json.dumps({'customers': customer})

def deleteCustomer(customer_id):
	dynamodb = get_db_client()
	
	response = dynamodb.delete_item(
		TableName=table_name,
		Key={
			'customer_id': {
				'S': customer_id
			}
		}
	)
	# logger.info("Logger Response: ")
	# logger.info(response)
	customer = {
		'data': {
			'customer_id' : customer_id,
		},
		'status' : 'DELETED OK'
	}
	return json.dumps({'customers': customer})