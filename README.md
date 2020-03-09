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
- Clone CodeCommit Repository and navigate to working directory
```bash
$ cd ~/environment
$ git clone https://git-codecommit.ap-southeast-2.amazonaws.com/v1/repos/myproject-customer-service-python
$ cd ~/environment/myproject-customer-service-python
```

- Follow folder structure
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

- Activate virtual environment, install flask and flask-cors
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ venv/bin/pip install flask
$ venv/bin/pip install flask-cors
```

- Add .gitignore file ~/environment/myproject-customer-service-python/.gitignore
- Add static database ~/environment/myproject-customer-service-python/customers.json
- Add customer routes ~/environment/myproject-customer-service-python/customer_routes.py
- Add app             ~/environment/myproject-customer-service-python/app.py
- Add custom logger   ~/environment/myproject-customer-service-python/custom_logger.py
- Add README.md file  ~/environment/myproject-customer-service-python/README.md
- Generate requirements.txt
```bash
$ pip freeze > requirements.txt
```

- (To Do) Add Unit Testing

- Run locally before dockerizing
```bash
$ python app.py
$ curl http://localhost:5000
```

- Test using curl scripts ~/environment/myproject-customer-service-python/curl_scripts.md

- Add Docker File ~/environment/myproject-customer-service-python/Dockerfile

- Build, Tag and Run the Docker Image locally. (Replace AccountId and Region)
```bash
$ docker build -t myproject-customer-service .
$ docker tag myproject-customer-service:latest 222337787619.dkr.ecr.ap-southeast-2.amazonaws.com/myproject-customer-service:latest
$ docker run -p 5000:5000 myproject-customer-service:latest
```

- Test using curl scripts ~/environment/myproject-customer-service-python/curl_scripts.md

- Push our Docker Image to ECR and validate
```bash
$ $(aws ecr get-login --no-include-email)
$ docker push 222337787619.dkr.ecr.ap-southeast-2.amazonaws.com/myproject-customer-service:latest
$ aws ecr describe-images --repository-name myproject-customer-service
```

- Make changes, commit and push changes to CodeCommit repository to trigger codepipeline deployment to EKS
```bash
$ git add .
$ git commit -m "Initial Commit"
$ git push origin master
```

- Test using curl scripts ~/environment/myproject-customer-service-python/curl_scripts.md

## (Optional) Clean up
```bash
$ aws ecr delete-repository --repository-name myproject-customer-service --force
$ aws codecommit delete-repository --repository-name myproject-customer-service
$ rm -rf ~/environment/myproject-customer-service
```
