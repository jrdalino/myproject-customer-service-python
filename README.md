# myproject-customer-service-python

## Functional Requirements
- Create, Read, Update, Delete, and List Customers

## API Endpoints
```
| HTTP METHOD | URI                                       | ACTION                       |
|-------------|-------------------------------------------|------------------------------|
| GET         | http://[hostname]/customers               | Gets all customers           |
| GET         | http://[hostname]/customers/<customer_id> | Gets one customer            |
| POST        | http://[hostname]/customers               | Creates a new customer       |
| PUT         | http://[hostname]/customers/<customer_id> | Updates an existing customer |
| DELETE      | http://[hostname]/customers/<customer_id> | Deletes a customer           |
```

## Prerequisites
- Docker, Python, Flask, Git, Virtualenv https://github.com/jrdalino/development-environment-setup
- Prepare DynamoDB table using https://github.com/jrdalino/myproject-aws-dynamodb-customer-service-terraform
- Setup CI/CD using https://github.com/jrdalino/myproject-aws-codepipeline-customer-service-terraform. This will create CodeCommit Repo, ECR Repo, CodeBuild Project, Lambda Function and CodePipeline Pipeline 
- Create ELB Service Role if it doesnt exist yet
```
$ aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing" || aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
```

## Structure and Environment
- Clone CodeCommit Repository and navigate to working directory
```bash
$ cd ~/environment
$ git clone https://git-codecommit.ap-southeast-2.amazonaws.com/v1/repos/myproject-customer-service && cd ~/environment/myproject-customer-service
```

- Follow folder structure as per https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/ and https://github.com/pallets/flask/tree/master/examples/tutorial
```
$ ~/environment/myproject-customer-service
├── flaskr/
│   ├── app.py
│   ├── auth.py
│   ├── custom_logger.py
│   ├── customer_routes.py
│   ├── db.py
│   ├── requirements.txt
│   └── schema.tf
├── kubernetes/
│   ├── deployment.yml
│   └── service.yml
├── tests/
│   ├── conftest.py
│   ├── customers.json
│   ├── test_auth_routes.py
│   ├── test_customer_routes.py
│   ├── test_curl.sh
│   ├── test_db.py
│   └── test_factory.py
├── venv/
├── .gitignore
├── buildspec.yml
├── Dockerfile
└── README.md
```

- Activate virtual environment, install flask and flask-cors
```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ venv/bin/pip install flask flask-cors boto3
(venv) $ deactivate # To deactivate
```

## Logging
- Add custom logger ~/environment/myproject-customer-service/flaskr/custom_logger.py

## Development
- Add static database ~/environment/myproject-customer-service/tests/customers.json
- Add customer dynamodb table client ~/environment/myproject-customer-service/flaskr/customer_table_client.py
- Add customer routes ~/environment/myproject-customer-service/flaskr/customer_routes.py
- Add app ~/environment/myproject-customer-service/flaskr/app.py
- You may also copy everything from Github repo to CodeCommit repo
```
$ rsync -rv --exclude=.git ~/environment/myproject-customer-service-python/ ~/environment/myproject-customer-service/
```

## Run
- Run locally
```bash
$ cd flaskr
$ chmod a+x app.py
$ ./app.py
$ curl http://localhost:5000
```

## Testing
- Add tests using curl ~/environment/myproject-customer-service/tests/test_curl.sh
- Replace hostname and port variables
- Run tests using curl
```
$ cd ~/environment/myproject-customer-service/tests
$ chmod a+x test_curl.sh
$ ./test_curl.sh
```
- Install pytest and coverage to test and measure your code
```
(venv) $ venv/bin/pip install pytest coverage
```
- Install pytest-flask and moto to mock your flask server and mock dynamodb 
```
(venv) $ venv/bin/pip install pytest-flask moto
```
- Add static database ~/environment/myproject-customer-service/tests/customers.json
- Add tests for factory ~/environment/myproject-customer-service/tests/test_factory.py
- Add tests for database ~/environment/myproject-customer-service/tests/test_db.py
- Add ~/environment/myproject-customer-service/tests/__init__.py
- Add tests for customer routes ~/environment/myproject-customer-service/tests/test_customer_routes.py
- Run tests and measure code coverage
```
$ pytest
$ coverage run -m pytest
$ coverage report
$ coverage html # open htmlcov/index.html in a browser
```
- TODO: Add tests for other AWS Services https://github.com/spulec/moto

## Containerize
- Generate ~/environment/myproject-customer-service/flaskr/requirements.txt
```bash
$ pip freeze > requirements.txt
```
- Add Docker File ~/environment/myproject-customer-service/Dockerfile
- Build, Tag and Run the Docker Image locally. (Replace AccountId and Region)
```bash
$ cd ~/environment/myproject-customer-service
$ docker build -t myproject-customer-service .
$ docker tag myproject-customer-service:latest 222337787619.dkr.ecr.ap-southeast-2.amazonaws.com/myproject-customer-service:latest
$ docker run -e AWS_ACCESS_KEY_ID=<REPLACE_ME> -e AWS_SECRET_ACCESS_KEY=<REPLACE_ME> -d -p 5000:5000 myproject-customer-service:latest
$ curl http://localhost:5000
```
- Note: For manual deployment only, create the image repositories manually
```bash
$ aws ecr create-repository --repository-name myproject-customer-service
```
- Push Docker Image to ECR and validate
```bash
$ $(aws ecr get-login --no-include-email)
$ docker push 222337787619.dkr.ecr.ap-southeast-2.amazonaws.com/myproject-customer-service:latest
$ aws ecr describe-images --repository-name myproject-customer-service
```

## Pre-Deployment
- Add .gitignore file ~/environment/myproject-customer-service/.gitignore
- Add Kubernetes Deployment and Service Yaml files ~/environment/myproject-customer-service/kubernetes/deployment.yml and ~/environment/myproject-customer-service/kubernetes/service.yml

## Manual Deployment
- Create k8s Deployment and Service
```
$ cd ~/environment/myproject-customer-service/kubernetes
$ kubectl apply -f deployment.yml
$ kubectl apply -f service.yml
$ kubectl get all
```

## Automated Deployment
- Review https://github.com/jrdalino/myproject-aws-codepipeline-customer-service-terraform
- Add Buildspec Yaml file ~/environment/myproject-customer-service/buildspec.yml
- Make changes, commit and push changes to CodeCommit repository to trigger codepipeline deployment to EKS
```bash
$ git add .
$ git commit -m "Initial Commit"
$ git push origin master
```
- Create k8s Service (You only have to do this once)
```
$ cd ~/environment/myproject-customer-service/kubernetes
$ kubectl apply -f service.yml
$ kubectl get all
```

## (Optional) Clean up
```bash
$ kubectl delete -f service.yml
$ kubectl delete -f deployment.yml
$ aws ecr delete-repository --repository-name myproject-customer-service --force
$ aws codecommit delete-repository --repository-name myproject-customer-service
$ rm -rf ~/environment/myproject-customer-service
$ docker ps
$ docker kill <CONTAINER_ID>
$ docker images
$ docker system prune -a
```