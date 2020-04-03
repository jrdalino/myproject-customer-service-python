import boto3
import json
import logging
from collections import defaultdict
import argparse
import uuid

import datetime
from datetime import date

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

def get_all_customers():
	dynamodb = get_db_client()
	response = dynamodb.scan(
		TableName=table_name
	)
	# logger.info("Logger Response: ")
	# logger.info(response)    
	customer_list = defaultdict(list)
	for item in response["Items"]:
		customer = {
			'customerId': item['customerId']['S'],
			'firstName': item['firstName']['S'],
			'lastName': item['lastName']['S'],
			'email': item['email']['S'],
			'userName': item['userName']['S'],
			'birthDate': item['birthDate']['S'],
			'gender': item['gender']['S'],
			'custNumber': item['custNumber']['S'],
			'cardNumber': item['cardNumber']['S'],
			'phoneNumber': item['phoneNumber']['S'],
			'createdDate': item['createdDate']['S'],
			'updatedDate': item['updatedDate']['S'],
			'profilePhotoUrl': item['profilePhotoUrl']['S'],
		}
		customer_list["customers"].append(customer)
	return json.dumps(customer_list)

def get_customer(customerId):
	dynamodb = get_db_client()
	response = dynamodb.get_item(
		TableName=table_name,
		Key={
			'customerId': {
				'S': customerId
			}
		}
	)
	# logger.info("Logger Response: ")
	# logger.info(response)
	item = response['Item']

	customer = {
		'customerId': item['customerId']['S'],
		'firstName': item['firstName']['S'],
		'lastName': item['lastName']['S'],
		'email': item['email']['S'],
		'userName': item['userName']['S'],
		'birthDate': item['birthDate']['S'],
		'gender': item['gender']['S'],
		'custNumber': item['custNumber']['S'], 
		'cardNumber': item['cardNumber']['S'], 
		'phoneNumber': item['phoneNumber']['S'],
		'createdDate': item['createdDate']['S'],
		'updatedDate': item['updatedDate']['S'],
		'profilePhotoUrl': item['profilePhotoUrl']['S'],
	}
	return json.dumps({'customer': customer})

def create_customer(customer_dict):
	dynamodb = get_db_client()
	customerId = str(uuid.uuid4())
	firstName = str(customer_dict['firstName'])
	lastName = str(customer_dict['lastName'])
	email = str(customer_dict['email'])
	userName = str(customer_dict['userName'])
	birthDate = str(customer_dict['birthDate'])
	gender = str(customer_dict['gender'])
	custNumber = str(customer_dict['custNumber']) # generate randon custNumber
	cardNumber = str(customer_dict['cardNumber']) # generate random, cardNumber
	phoneNumber = str(customer_dict['phoneNumber'])
	createdDate = str(datetime.datetime.now().isoformat())
	updatedDate = "1900-01-01T00:00:00.000000"
	profilePhotoUrl = str(customer_dict['profilePhotoUrl'])
	response = dynamodb.put_item(
		TableName=table_name,
		Item={
				'customerId': {
					'S': customerId
				},
				'firstName': {
					'S' : firstName
				},
				'lastName': {
					'S' : lastName
				},                
				'email' : {
					'S' : email
				},
				'userName' : {
					'S' : userName
				},
				'birthDate': {
					'S' : birthDate
				},
				'gender': {
					'S' : gender
				},
				'custNumber': {
					'S' : custNumber
				},
				'cardNumber': {
					'S' : cardNumber
				},
				'phoneNumber': {
					'S' : phoneNumber
				},
				'createdDate': {
					'S' : createdDate
				},
				'updatedDate': {
					'S' : updatedDate
				},
				'profilePhotoUrl': {
					'S' : profilePhotoUrl
				}				
			}
		)
	# logger.info("Logger Response: ")
	# logger.info(response)
	customer = {
		'customerId': customerId,
		'firstName': firstName,
		'lastName': lastName,
		'email': email,
		'userName': userName,
		'birthDate': birthDate,
		'gender': gender,
		'custNumber': custNumber,
		'cardNumber': cardNumber,
		'phoneNumber': phoneNumber,
		'createdDate': createdDate,
		'updatedDate': updatedDate,
		'profilePhotoUrl': profilePhotoUrl,
	}
	return json.dumps({'customer': customer})

def update_customer(customerId, customer_dict):
	dynamodb = get_db_client()
	firstName = str(customer_dict['firstName'])
	lastName = str(customer_dict['lastName'])
	email = str(customer_dict['email'])
	userName = str(customer_dict['userName'])
	birthDate = str(customer_dict['birthDate'])
	gender = str(customer_dict['gender'])
	# custNumber = str(customer_dict['custNumber'])
	# cardNumber = str(customer_dict['cardNumber'])
	phoneNumber = str(customer_dict['phoneNumber'])
	# createdDate = str(customer_dict['createdDate'])
	updatedDate = str(datetime.datetime.now().isoformat())
	profilePhotoUrl = str(customer_dict['profilePhotoUrl'])
	response = dynamodb.update_item(
		TableName=table_name,
		Key={
			'customerId': {
				'S': customerId
			}
		},
		UpdateExpression="""SET firstName = :p_firstName,
								lastName = :p_lastName,
								email = :p_email,
								userName = :p_userName,
								birthDate = :p_birthDate,
								gender = :p_gender,
								phoneNumber = :p_phoneNumber,
								updatedDate = :p_updatedDate,
								profilePhotoUrl = :p_profilePhotoUrl
								""",
		ExpressionAttributeValues={
			':p_firstName': {
				'S' : firstName
			},
			':p_lastName' : {
				'S' : lastName
			},
			':p_email': {
				'S' : email
			},
			':p_userName': {
				'S' : userName
			},
			':p_birthDate': {
				'S' : birthDate
			},
			':p_gender': {
				'S' : gender
			},
			':p_phoneNumber': {
				'S' : phoneNumber
			},
			':p_updatedDate': {
				'S' : updatedDate
			},
			':p_profilePhotoUrl': {
				'S' : profilePhotoUrl
			}
		}
	)
	# logger.info("Logger Response: ")
	# logger.info(response)
	customer = {
		'customerId': customerId,
		'firstName': firstName,
		'lastName': lastName,
		'email': email,
		'userName': userName,
		'birthDate': birthDate,
		'gender': gender,
		# 'custNumber': custNumber,
		# 'cardNumber': cardNumber,
		'phoneNumber': phoneNumber,
		# 'createdDate': createdDate,
		'updatedDate': updatedDate,
		'profilePhotoUrl': profilePhotoUrl,
	}
	return json.dumps({'customer': customer})

def delete_customer(customerId):
	dynamodb = get_db_client()
	response = dynamodb.delete_item(
		TableName=table_name,
		Key={
			'customerId': {
				'S': customerId
			}
		}
	)
	# logger.info("Logger Response: ")
	# logger.info(response)
	customer = {
		'customerId' : customerId,
	}
	return json.dumps({'customer': customer})

def customer_number_generator():
	now = datetime.datetime.now()
	# get latest id from db and increment
	new_customer_number = '099996' + str(now.year) + str(now.month) + str(now.day) + '01'
	return new_customer_number

def card_number_generator():
	now = datetime.datetime.now()
	# get latest id from db and increment
	new_card_number = '623633' + str(now.year) + str(now.month) + str(now.day) + '00001'
	return new_card_number