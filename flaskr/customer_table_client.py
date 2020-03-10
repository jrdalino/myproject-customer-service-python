import boto3
import json
import logging
from collections import defaultdict
import argparse

client = boto3.client('dynamodb', region_name='ap-southeast-2')

def get_customers_json(items):
    # loop through the returned customers and add their attributes to a new dict
    # that matches the JSON response structure expected by the frontend.
    customer_list = defaultdict(list)

    for item in items:
        customer = {}

        customer["customer_id"] = item["customer_id"]["S"]
        customer["first_name"] = item["first_name"]["S"]
        customer["last_name"] = item["last_name"]["S"]
        customer["email"] = item["email"]["S"]
        customer["dob"] = item["dob"]["S"]
        customer["gender"] = item["gender"]["S"]

        customer_list["customers"].append(customer)

    return customer_list

def get_all_customers_ddb():
    response = client.scan(
        TableName='customers'
    )

    logging.info(response["Items"])

    # loop through the returned customers and add their attributes to a new dict
    # that matches the JSON response structure expected by the frontend.
    customer_list = get_customers_json(response["Items"])

    return json.dumps(customer_list)