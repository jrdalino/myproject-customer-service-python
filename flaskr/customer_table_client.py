import boto3
import json
import logging
from collections import defaultdict
import argparse
import uuid

import datetime
from datetime import date

from boto3.dynamodb.conditions import Key, Attr

if __package__ is None or __package__ == '':
	# uses current directory visibility
	from custom_logger import setup_logger
	from db import get_db_client, get_db_resource
else:
	# uses current package visibility
	from flaskr.custom_logger import setup_logger
	from flaskr.db import get_db_client, get_db_resource


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
	
	customerId = str(uuid.uuid4())
	firstName = str(customer_dict['firstName'])
	lastName = str(customer_dict['lastName'])
	email = str(customer_dict['email'])
	userName = str(customer_dict['userName'])
	birthDate = str(customer_dict['birthDate'])
	gender = str(customer_dict['gender'])
	custNumber = customer_number_generator()
	cardNumber = card_number_generator()
	phoneNumber = str(customer_dict['phoneNumber'])
	createdDate = str(datetime.datetime.now().isoformat())
	updatedDate = "1900-01-01T00:00:00.000000"
	profilePhotoUrl = str(customer_dict['profilePhotoUrl'])

	# check if is_unique
	unique = is_unique(customerId, email, userName, custNumber, cardNumber)
		
	if len(unique) == 0:

		dynamodb = get_db_client()
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

	else: 

		return json.dumps({'customer': 'The following values already exist in the database {}'.format(unique)})


def update_customer(customerId, customer_dict):
	dynamodb = get_db_client()
	firstName = str(customer_dict['firstName'])
	lastName = str(customer_dict['lastName'])
	email = str(customer_dict['email'])
	userName = str(customer_dict['userName'])
	birthDate = str(customer_dict['birthDate'])
	gender = str(customer_dict['gender'])
	phoneNumber = str(customer_dict['phoneNumber'])
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
		},
		ReturnValues="ALL_NEW"
	)
	# logger.info("Logger Response: ")
	# logger.info(response)
	updated = response['Attributes']
	customer = {
		'customerId': updated['customerId']['S'],
		'firstName': updated['firstName']['S'],
		'lastName': updated['lastName']['S'],
		'email': updated['email']['S'],
		'userName': updated['userName']['S'],
		'birthDate': updated['birthDate']['S'],
		'gender': updated['gender']['S'],
		'custNumber': updated['custNumber']['S'],
		'cardNumber': updated['cardNumber']['S'],
		'phoneNumber': updated['phoneNumber']['S'],
		'createdDate': updated['createdDate']['S'],
		'updatedDate': updated['updatedDate']['S'],
		'profilePhotoUrl': updated['profilePhotoUrl']['S'],
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


def is_unique(customerId, email, userName, custNumber, cardNumber):
	"""
	Checks if email, userName, custNumber, cardNumber are unique
	Will return a list do duplicate fields
	"""
	dynamodb = get_db_resource()

	table = dynamodb.Table(table_name)

	filter_expression = Attr('customerId').eq(customerId) \
		| Attr('email').eq(email) \
		| Attr('userName').eq(userName) \
		| Attr('custNumber').eq(custNumber) \
		| Attr('cardNumber').eq(cardNumber)

	response = table.scan(
		Select='ALL_ATTRIBUTES',
		FilterExpression=filter_expression,
		ConsistentRead=True,
	)


	duplicate_fields = []

	if len(response['Items']) == 0: 

		return duplicate_fields
	
	else: 

		if response['Items'][0]['customerId'] == customerId:

			duplicate_fields.append('customerId : {}'.format(customerId))

		if response['Items'][0]['email'] == email:

			duplicate_fields.append('email : {}'.format(email))

		if response['Items'][0]['userName'] == userName:

			duplicate_fields.append('userName : {}'.format(userName))

		if response['Items'][0]['custNumber'] == custNumber:

			duplicate_fields.append('custNumber : {}'.format(custNumber))

		if response['Items'][0]['cardNumber'] == cardNumber:

			duplicate_fields.append('cardNumber : {}'.format(cardNumber))

	return duplicate_fields



def get_max_value(attribute):

	"""Will scan the table for the maximum possible value given an attribute"""

	dynamodb = get_db_client()

	maximum = None

	response = dynamodb.scan(
		TableName=table_name,
		Select='SPECIFIC_ATTRIBUTES',
	 	AttributesToGet=[
	 		attribute
	  ],
		ConsistentRead=True,
	)

	if response['Items'] == []: 
		pass
	else: 

		maximum = max([int(m[attribute]['S']) for m in response['Items']])

	return maximum


def customer_number_generator():
	now = datetime.datetime.now()

	max_value = get_max_value('custNumber')

	if max_value: 
		# get latest id from db and increment
		# get last 2 digits
		last_digits = str(max_value)[-2:]
		logger.info("last digits")
		logger.info(last_digits)
		new_customer_number = '099996' + str(now.year) + str(now.month) + str(now.day) + str(int(last_digits) + 1).zfill(2)

	else: 

		new_customer_number = '099996' + str(now.year) + str(now.month) + str(now.day) + '01'

	return new_customer_number

def card_number_generator():
	now = datetime.datetime.now()

	max_value = get_max_value('cardNumber')

	if max_value: 
		# get last 5 digits
		last_digits = str(max_value)[-5:]
			
		new_card_number = '623633' + str(now.year) + str(now.month) + str(now.day) + str(int(last_digits) + 1).zfill(5)

	else: 

		new_card_number = '623633' + str(now.year) + str(now.month) + str(now.day) + '00001'

	return new_card_number