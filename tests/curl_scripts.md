- Test Get All Customers
```bash
curl -X GET \
  http://localhost:5000/customers \
  -H 'Host: localhost:5000'
```

- Test Get Customer
```bash
curl -X GET \
  http://localhost:5000/customers/4e53920c-505a-4a90-a694-b9300791f0ae \
  -H 'Host: localhost:5000' 
```

- Test Create Customer
```bash
curl -X POST \
  http://localhost:5000/customers \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name":"New Customer First Name",
  "last_name": "New Customer Last Name",
  "email": "first.last@example.com", 
  "dob": "January 1, 1900",    
  "gender": "Female"
}'
```

- Test Update Customer
```bash
curl -X PUT \
  http://localhost:5000/customers/4e53920c-505a-4a90-a694-b9300791f0ae \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name":"Barnie v2",
  "last_name": "Whittam v2",
  "email": "bwhittam0@cpanel.net v2", 
  "dob": "December 31, 1999 v2",    
  "gender": "Male v2"
}'
```

- Test Delete Customer
```bash
curl -X DELETE \
  http://localhost:5000/customers/4e53920c-505a-4a90-a694-b9300791f0ae \
  -H 'Content-Type: application/json'
```