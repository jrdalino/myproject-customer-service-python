import boto3
import json
import logging
from collections import defaultdict
import argparse
import uuid
import time
if __package__ is None or __package__ == '':
	# uses current directory visibility
	from custom_logger import setup_logger
	from db import get_db_client
else:
	# uses current package visibility
	from flaskr.custom_logger import setup_logger
	from flaskr.db import get_db_client

logger = setup_logger(__name__)
tableName = 'customers'

def getAllCustomers():
	dynamodb = get_db_client()
	response = dynamodb.scan(
		TableName=tableName
	)
	# logger.info("Logger Response: ")
	# logger.info(response)    
	customerList = defaultdict(list)
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
		customerList["customers"].append(customer)
	return json.dumps(customerList)

def getCustomer(customerId):
	dynamodb = get_db_client()
	response = dynamodb.get_item(
		TableName=tableName,
		Key={
			'customerId': {
				'S': customerId
			}
		}
	)
	# logger.info("Logger Response: ")
	# logger.info(response)
	if 'Item' in response:
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

def createCustomer(customerDict):
	dynamodb = get_db_client()
	customerId = str(uuid.uuid4())
	firstName = str(customerDict['firstName'])
	lastName = str(customerDict['lastName'])
	email = str(customerDict['email'])
	userName = str(customerDict['userName'])
	birthDate = str(customerDict['birthDate'])
	gender = str(customerDict['gender'])
	custNumber = str(customerDict['custNumber']) # generate randon custNumber
	cardNumber = str(customerDict['cardNumber']) # generate randp, cardNumber
	phoneNumber = str(customerDict['phoneNumber'])
	createdDate = str(time.time()) # str(customerDict['createdDate'])
	updatedDate = str(customerDict['updatedDate'])
	profilePhotoUrl = str(customerDict['profilePhotoUrl'])
	response = dynamodb.put_item(
		TableName=tableName,
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
		'data' : {
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
		},
		'status' : 'CREATED OK'
	}
	return json.dumps({'customers': customer})

def updateCustomer(customerId, customerDict):
	dynamodb = get_db_client()
	firstName = str(customerDict['firstName'])
	lastName = str(customerDict['lastName'])
	email = str(customerDict['email'])
	userName = str(customerDict['userName'])
	birthDate = str(customerDict['birthDate'])
	gender = str(customerDict['gender'])
	custNumber = str(customerDict['custNumber'])
	cardNumber = str(customerDict['cardNumber'])
	phoneNumber = str(customerDict['phoneNumber'])
	createdDate = str(customerDict['createdDate'])
	updatedDate = str(time.time()) # str(customerDict['updatedDate'])
	profilePhotoUrl = str(customerDict['profilePhotoUrl'])
	response = dynamodb.update_item(
		TableName=tableName,
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
								custNumber = :p_custNumber,
								cardNumber = :p_cardNumber,
								phoneNumber = :p_phoneNumber,
								createdDate = :p_createdDate,
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
			':p_custNumber': {
				'S' : custNumber
			},
			':p_cardNumber': {
				'S' : cardNumber
			},
			':p_phoneNumber': {
				'S' : phoneNumber
			},
			':p_createdDate': {
				'S' : createdDate
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
		'data' : {
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
		},
		'status' : 'UPDATED OK'
	}
	return json.dumps({'customers': customer})

def deleteCustomer(customerId):
	dynamodb = get_db_client()
	response = dynamodb.delete_item(
		TableName=tableName,
		Key={
			'customerId': {
				'S': customerId
			}
		}
	)
	# logger.info("Logger Response: ")
	# logger.info(response)
	customer = {
		'data': {
			'customerId' : customerId,
		},
		'status' : 'DELETED OK'
	}
	return json.dumps({'customers': customer})