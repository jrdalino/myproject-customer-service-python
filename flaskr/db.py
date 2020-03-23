import boto3

def get_db_client():
		dynamodb = boto3.client('dynamodb', 
				region_name='ap-southeast-2',
		)
		return dynamodb