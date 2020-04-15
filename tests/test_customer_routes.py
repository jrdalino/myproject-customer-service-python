import pytest
import unittest
import boto3
import sys 
from moto import mock_dynamodb2
from flaskr.customer_table_client import get_all_customers, get_customer, \
	create_customer, update_customer, delete_customer
import json
import os

# Load customers static db from json file
THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
my_file = os.path.join(THIS_FOLDER, "tests", 'customers.json')

with open(my_file) as f:
    customers = json.load(f)

class TestDynamo(unittest.TestCase):
		def setUp(self):
			self.table_name = 'customers'
			# load the test data from test/customers.json
			self.customer_data = {
				"customers": customers
			}
			self.test_customer_id = '4e53920c-505a-4a90-a694-b9300791f0ae'
			self.test_delete_customer_id = "2b473002-36f8-4b87-954e-9a377e0ccbec"
			self.test_customer_dict = {
					"firstName": "Mikhael",
					"lastName": "Cuazon",
					"email": "Mikhael@cpanel.net",
					"userName": "Mikhael@cpanel.net",
					"birthDate": "January 17, 1996",
					"gender": "Male",
					"custNumber": "0999962019111902",
					"cardNumber": "6236332019111900012",
					"custAccountNo": "0000000000000000000000",				
					"phoneNumber": "97667322",
					"createdDate": "March 27, 2020",
					"updatedDate": "March 27, 2020",
					"profilePhotoUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/PICA.jpg/600px-PICA.jpg"
			}

		@mock_dynamodb2
		def __moto_dynamodb_setup(self):
				table_name = 'customers'
				dynamodb = boto3.resource('dynamodb', 'ap-southeast-2')
				table = dynamodb.create_table(
						TableName=table_name,
						KeySchema=[
								{
										'AttributeName': 'customerId',
										'KeyType': 'HASH'
								},
						],
						AttributeDefinitions=[
								{
										'AttributeName': 'customerId',
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
						item['customerId'] = customer['customerId']
						item['firstName'] = customer['firstName']
						item['lastName'] = customer['lastName']
						item['email'] = customer['email']
						item['userName'] = customer['userName']
						item['birthDate'] = customer['birthDate']
						item['gender'] = customer['gender']
						item['custNumber'] = customer['custNumber']
						item['cardNumber'] = customer['cardNumber']
						item['custAccountNo'] = customer['custAccountNo']						
						item['phoneNumber'] = customer['phoneNumber']
						item['createdDate'] = customer['createdDate']
						item['updatedDate'] = customer['updatedDate']
						item['profilePhotoUrl'] = customer['profilePhotoUrl']								
						table.put_item(Item=item)

		@mock_dynamodb2
		def test_get_all_customers(self):
				self.__moto_dynamodb_setup()
				customers = get_all_customers()
				self.assertEqual(json.dumps(self.customer_data), customers)

		@mock_dynamodb2
		def test_get_customer(self):
				self.__moto_dynamodb_setup()
				customer = get_customer(self.test_customer_id)
				testCustomer = [c for c in self.customer_data['customers'] if c['customerId'] == self.test_customer_id]				
				# check if the data matches the sample data
				self.assertEqual(json.loads(customer)['customer'], testCustomer[0])

		@mock_dynamodb2
		def test_create_customer(self):
				self.__moto_dynamodb_setup()
				customer = create_customer(self.test_customer_dict)
				print(customer)
				createdId = json.loads(customer)['customer']['customerId']
				customerGet = get_customer(createdId)
				# check if the data key matches the created customer object
				self.assertEqual(json.loads(customer)['customer'], json.loads(customerGet)['customer'])

		@mock_dynamodb2
		def test_update_customer(self):
				self.__moto_dynamodb_setup()
				customer = update_customer(self.test_customer_id, self.test_customer_dict)
				updatedId = json.loads(customer)['customer']['customerId']
				customerGet = get_customer(updatedId)
				# check if the data key matches the updated customer object
				self.assertEqual(json.loads(customer)['customer'], json.loads(customerGet)['customer'])

		# @mock_dynamodb2
		# def test_delete_customer(self):
		# 		self.__moto_dynamodb_setup()
		# 		customer = delete_customer(self.test_delete_customer_id)
		# 		# check if the status is DELETED OK
		# 		self.assertEqual(json.loads(customer)['customers']['status'], "DELETED OK")
		# 		deletedId = json.loads(customer)['customers']['data']['customerId']
		# 		customerGet = get_customer(deletedId)
		# 		# check if the customerId matches the deleted object
		# 		self.assertEqual(deletedId, self.test_delete_customer_id)
		# 		# check if the customer exists will fail if existing
		# 		self.assertEqual(json.loads(customerGet)['customers']['status'], "Customer not found")