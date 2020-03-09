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
  "name":"Product G",
  "description": "Nulla nec",
  "image_url": "https://via.placeholder.com/200"
}'
```

- Test Update Customer
```bash
curl -X PUT \
  http://localhost:5000/customers/4e53920c-505a-4a90-a694-b9300791f0ae \
  -H 'Content-Type: application/json' \
  -d '{
  "name":"egg 123",
  "description": "my working description dasdasds",
  "image_url": "product_image testes update test"
}'
```

- Test Delete Customer
```bash
curl -X DELETE \
  http://localhost:5000/customers/4e53920c-505a-4a90-a694-b9300791f0ae \
  -H 'Content-Type: application/json'
```
