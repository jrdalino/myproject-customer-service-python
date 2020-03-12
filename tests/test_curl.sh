#!/bin/bash

# replace variables
hostname=localhost
port=5000
customer_id=4e53920c-505a-4a90-a694-b9300791f0ae

echo "test get all customers"
echo "----------------------"
curl -X GET \
  http://$hostname:$port/customers \
  -H 'Host: $hostname:$port'
echo
echo

echo "test get customer by id"
echo "-----------------------"
curl -X GET \
  http://$hostname:$port/customers/$customer_id \
  -H 'Host: $hostname:$port' 
echo
echo

echo "test create a new customer"
echo "--------------------------"
curl -X POST \
  http://$hostname:$port/customers \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name":"New Customer First Name",
  "last_name": "New Customer Last Name",
  "email": "first.last@example.com", 
  "dob": "February 1, 1900",    
  "gender": "Female"
}'
echo
echo

echo "test update customer by id"
echo "--------------------------"
curl -X PUT \
  http://$hostname:$port/customers/$customer_id \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name":"New Customer First Name v2",
  "last_name": "New Customer Last Name v2",
  "email": "first.last@example.com v2", 
  "dob": "February 1, 1900 v2",    
  "gender": "Female v2"
}'
echo
echo

echo "test delete customer by id"
echo "--------------------------"
curl -X DELETE \
  http://$hostname:$port/customers/$customer_id \
  -H 'Content-Type: application/json'
echo
echo

exit 0