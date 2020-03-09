# myproject-customer-service-python

## API Endpoints
```
| HTTP METHOD | URI                                      | ACTION                       |
|-------------|------------------------------------------|------------------------------|
| GET         | http://[hostname]/customers              | Gets all customers           |
| GET         | http://[hostname]/customers/<customerId> | Gets one customer            |
| POST        | http://[hostname]/customers              | Creates a new customer       |
| PUT         | http://[hostname]/customers/<customerId> | Updates an existing customer |
| DELETE      | http://[hostname]/customers/<customerId> | Deletes a customer           |
```

## Prerequisites
- Setup CI/CD using https://github.com/jrdalino/myproject-aws-codepipeline-customer-service-terraform. This will create CodeCommit Repo, ECR Repo, CodeBuild Project, Lambda Function and CodePipeline Pipeline 
- You may also create the repositories individually
```bash
$ aws codecommit create-repository --repository-name myproject-customer-service
$ aws ecr create-repository --repository-name myproject-customer-service
```

- Prepare DynamoDB table using https://github.com/jrdalino/myproject-aws-dynamodb-customer-service-terraform

## Usage
- Clone CodeCommit Repository
```bash
$ cd ~/environment
$ git clone https://git-codecommit.ap-southeast-2.amazonaws.com/v1/repos/myproject-customer-service-python
```

- Prepare folder structure
```
~/environment/myproject-customer-service-python
├── app.py
├── custom_logger.py
├── customer_routes.py
├── customers.json
├── requirements.txt
├── venv/
├── Dockerfile
├── README.md
└── .gitignore
```

- Add .gitignore file
```bash
$ cd ~/environment/myproject-customer-service-python
$ touch .gitignore
```

- Navigate to working directory
```bash
$ cd ~/environment/myproject-customer-service-python
$ python3 -m venv venv
$ source venv/bin/activate
$ venv/bin/pip install flask
$ venv/bin/pip install flask-cors
```

- Prepare static database for testing
```bash
$ cd ~/environment/myproject-customer-service-python
$ touch customers.json
```

- Add customer_routes.py
```bash
$ cd ~/environment/myproject-customer-service-python
$ touch customer_routes.py
```

- Add app.py
```bash
$ cd ~/environment/myproject-customer-service-python
$ vi app.py
```

- Add custom_logger.py
```bash
$ cd ~/environment/myproject-customer-service-python
$ vi custom_logger.py
```

- Run locally and test
```bash
$ cd ~/environment/myproject-customer-service-python
$ python app.py
$ curl http://localhost:5000
```

- Generate requirements.txt
```bash
$ cd ~/environment/myproject-customer-service-python
$ pip freeze > requirements.txt
```

- Create the Docker file
```bash
$ cd ~/environment/myproject-customer-service-python
$ touch Dockerfile
```

- Build, Tag and Run the Docker Image locally. Replace AccountId and Region
```bash
$ docker build -t myproject-customer-service .
$ docker tag myproject-customer-service:latest 707538076348.dkr.ecr.ap-southeast-1.amazonaws.com/myproject-customer-service:latest
$ docker run -p 5000:5000 myproject-customer-service:latest
```

### User Acceptance Testing
- Test Get all Customers
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

### (To Do) Unit Testing

### Deployment
- Deploy to ECR
```bash
$ $(aws ecr get-login --no-include-email)
```

- Push our Docker Image and validate
```bash
$ docker push 222337787619.dkr.ecr.ap-southeast-2.amazonaws.com/myproject-customer-service:latest
$ aws ecr describe-images --repository-name myproject-customer-service
```

### (Optional) Clean up
```bash
$ aws ecr delete-repository --repository-name myproject-customer-service --force
$ aws codecommit delete-repository --repository-name myproject-customer-service
$ rm -rf ~/environment/myproject-customer-service
```
