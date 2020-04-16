#!/bin/bash

# replace variables
hostname=localhost
port=5000
customerId=c36262f5-61d9-484c-ae4a-4a8587980965

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
  "firstName":"New Customer First Name v3",
  "lastName": "New Customer Last Name v3",
  "email": "first.last.v3@example.com",
  "userName": "first.last.v3@example.com", 
  "birthDate": "1973-12-31T00:00:00.000000",    
  "gender": "Male",
  "phoneNumber" : "12345678",
  "custAccountNo" : "0000000000000000000003",
	"profilePhotoUrl": "http://example.com/helloV3.jpeg"
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