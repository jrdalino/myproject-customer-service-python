import boto3
import moto
import unittest

from flaskr.db import get_db_resource

class TestDb(unittest.TestCase):
	def set_up():
		pass

	def test_get_db_resource(self):
		dynamodb = get_db_resource()
		self.assertEqual(dynamodb._endpoint.host, 'https://dynamodb.ap-southeast-2.amazonaws.com')