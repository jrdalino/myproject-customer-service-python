import boto3
import json
import logging
from collections import defaultdict
import argparse
import uuid
from custom_logger import setup_logger

logger = setup_logger(__name__)
dynamodb = boto3.client('dynamodb', region_name='ap-southeast-2')
table_name = 'customers'

def getAllCustomers():
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
        }
        customer_list["customers"].append(customer)
    return json.dumps(customer_list)

def getCustomer(customer_id):
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
    item = response["Item"]
    customer = {
        'customer_id': item["customer_id"]["S"],
        'first_name': item['first_name']['S'],
        'last_name': item['last_name']['S'],            
        'email': item['email']['S'],
        'dob': item['dob']['S'],
        'gender': item['gender']['S'],
    }
    return json.dumps({'customers': customer})

def createCustomer(customer_dict):
    customer_id = str(uuid.uuid4())
    first_name = str(customer_dict['first_name'])
    last_name = str(customer_dict['last_name'])    
    email = str(customer_dict['email'])
    dob = str(customer_dict['dob'])
    gender = str(customer_dict['gender'])
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
                }
            }
        )
    # logger.info("Logger Response: ")
    # logger.info(response)
    customer = {
        'customer_id': customer_id,
        'first_name': first_name,
        'last_name': last_name,        
        'email': email,
        'dob': dob,
        'gender': gender,
        'status' : 'CREATED OK'
    }
    return json.dumps({'customers': customer})

def updateCustomer(customer_id, customer_dict):
    first_name = str(customer_dict['first_name'])
    last_name = str(customer_dict['last_name'])
    email = str(customer_dict['email'])
    dob = str(customer_dict['dob'])
    gender = str(customer_dict['gender'])    
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
                                gender = :p_gender
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
            }              
        }
    )
    # logger.info("Logger Response: ")
    # logger.info(response)
    customer = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'dob': dob,
        'gender': gender,        
        'status' : 'UPDATED OK'
    }
    return json.dumps({'customers': customer})

def deleteCustomer(customer_id):
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
        'customer_id' : customer_id,
        'status' : 'DELETED OK'
    }
    return json.dumps({'customers': customer})