import pytest
import unittest
import boto3
import sys 


from moto import mock_dynamodb2
from flaskr.customer_table_client import (getAllCustomers, getCustomer)
from flaskr.db import get_db_client
import json

class TestDynamo(unittest.TestCase):

    def setUp(self):
        self.table_name = 'customers'

        self.customer_data = {
          "customers": [
            {
              "customer_id": "4e53920c-505a-4a90-a694-b9300791f0ae",
              "first_name": "Barnie",
              "last_name": "Whittam",
              "email": "bwhittam0@cpanel.net",
              "dob": "December 31, 1999",
              "gender": "Male"
            },
            {
              "customer_id": "2b473002-36f8-4b87-954e-9a377e0ccbec",
              "first_name": "Emelyne",
              "last_name": "Plumley",
              "email": "eplumley1@wikipedia.org",
              "dob": "January 1, 2000",
              "gender": "Female"
            },
            {
              "customer_id": "3f0f196c-4a7b-43af-9e29-6522a715342d",
              "first_name": "Linoel",
              "last_name": "Dafter",
              "email": "ldafter2@ucsd.edu",
              "dob": "June 15, 1980",
              "gender": "Male"
            }
          ]
        }
        self.dynamodb = get_db_client()


    @mock_dynamodb2
    def __moto_dynamodb_setup(self):
        

        table_name = 'customers'
        dynamodb = boto3.resource('dynamodb', 'ap-southeast-2')

        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'customer_id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'customer_id',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )


        for customer in self.customer_data['customers']:

            item = {}
            item['customer_id'] = customer['customer_id']
            item['first_name'] = customer['first_name']
            item['last_name'] = customer['last_name']
            item['email'] = customer['email']
            item['dob'] = customer['dob']
            item['gender'] = customer['gender']
            table.put_item(Item=item)


    @mock_dynamodb2
    def test_get_all_customers(self):

        self.__moto_dynamodb_setup()

        customers = getAllCustomers()

        self.assertEqual(json.dumps(self.customer_data), customers)



    def test_get_customer(self):

        self.__moto_dynamodb_setup()

        customer = getCustomer("4e53920c-505a-4a90-a694-b9300791f0ae")

        self.assertEqual(json.dumps(self.customer_data['customers'][0]), customer)











