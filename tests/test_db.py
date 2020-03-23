import boto3
import moto
import unittest

from flaskr.db import get_db_client

class TestDb(unittest.TestCase):
	def set_up():
		pass

	def test_get_client(self):
		dynamodb = get_db_client()
		self.assertEqual(dynamodb._endpoint.host, 'https://dynamodb.ap-southeast-2.amazonaws.com')