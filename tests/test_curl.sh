#!/bin/bash

# replace variables
hostname=localhost
port=5000
customerId=0431af2b-71a5-4452-9600-7b26886d9b07

echo "test create a new customer"
echo "--------------------------"
curl -X POST \
  http://$hostname:$port/customers \
  -H 'Content-Type: application/json' \
  -d '{
  "firstName":"New Customer First Name",
  "lastName": "New Customer Last Name",
  "email": "first.last@example.com",
  "userName": "7c6e86fa-c319-45f7-beb0-0fec6020b458", 
  "birthDate": "1972-01-01T00:00:00.000000",    
  "gender": "Female",
  "phoneNumber" : "97667324",
  "profilePhotoUrl": "http://example.com/hello.jpeg"
}'
echo
echo

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
  http://$hostname:$port/customers/$customerId \
  -H 'Host: $hostname:$port' 
echo
echo

echo "test update customer by id"
echo "--------------------------"
curl -X PUT \
  http://$hostname:$port/customers/$customerId \
  -H 'Content-Type: application/json' \
  -d '{
  "firstName":"New Customer First Name v2",
  "lastName": "New Customer Last Name v2",
  "email": "first.last.v2@example.com",
  "userName": "first.last.v2@example.com", 
  "birthDate": "1972-12-31T00:00:00.000000",    
  "gender": "Female",
  "phoneNumber" : "12345678",
  "custAccountNo" : "0000000000000000000001",
	"profilePhotoUrl": "http://example.com/helloV2.jpeg"
}'
echo
echo

echo "test delete customer by id"
echo "--------------------------"
curl -X DELETE \
  http://$hostname:$port/customers/$customerId \
  -H 'Content-Type: application/json'
echo
echo

exit 0