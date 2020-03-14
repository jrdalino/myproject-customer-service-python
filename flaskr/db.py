
import boto3


def get_db_client():

		dynamodb = dynamodb = boto3.client('dynamodb', 
				region_name='ap-southeast-2',
				aws_access_key_id='x',
        aws_secret_access_key='x'
				)

		return dynamodb

