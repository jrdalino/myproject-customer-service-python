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
- Setup CI/CD using https://github.com/jrdalino/myproject-aws-codepipeline-customer-service-terraform. This will create CodeCommit Repo, ECR Repo, CodeBuild Project, Lambda Function and CodePipeline Pipeline 
- You may also create the repositories manually
```bash
$ aws codecommit create-repository --repository-name myproject-customer-service
$ aws ecr create-repository --repository-name myproject-customer-service
```

- Prepare DynamoDB table using https://github.com/jrdalino/myproject-aws-dynamodb-customer-service-terraform

## Usage
- Clone CodeCommit Repository and navigate to working directory
```bash
$ cd ~/environment
$ git clone https://git-codecommit.ap-southeast-2.amazonaws.com/v1/repos/myproject-customer-service
$ cd ~/environment/myproject-customer-service
```

- Follow folder structure
```
~/environment/myproject-customer-service
├── kubernetes/
│   ├── deployment.yml
│   └── service.yml
├── venv/
├── .gitignore
├── app.py
├── buildspec.yml
├── curl_scripts.md
├── custom_logger.py
├── customer_routes.py
├── customers.json
├── Dockerfile
├── README.md
├── requirements.txt
└── test_customer_routes.py
```

- Activate virtual environment, install flask and flask-cors
```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $
(venv) $ venv/bin/pip install flask
(venv) $ venv/bin/pip install flask-cors
```

- To deactivate
```bash
(venv) $ deactivate
```

- Add .gitignore file ~/environment/myproject-customer-service/.gitignore
- Add static database ~/environment/myproject-customer-service/customers.json
- Add custom logger   ~/environment/myproject-customer-service/custom_logger.py
- Add customer routes ~/environment/myproject-customer-service/customer_routes.py
- Add app             ~/environment/myproject-customer-service/app.py
- Add README.md file  ~/environment/myproject-customer-service/README.md
- Generate            ~/environment/myproject-customer-service/requirements.txt
```bash
$ pip freeze > requirements.txt
```

- (To Do) Add Unit Testing ~/environment/myproject-customer-service/test_customer_routes.py

- (To Do) Run Tests

- Run locally before dockerizing
```bash
$ chmod a+x app.py
$ ./app.py
$ curl http://localhost:5000
```

OR

```bash
$ python app.py
$ curl http://localhost:5000
```

- Test using curl scripts ~/environment/myproject-customer-service/curl_scripts.md

- Add Docker File ~/environment/myproject-customer-service/Dockerfile

- Build, Tag and Run the Docker Image locally. (Replace AccountId and Region)
```bash
$ docker build -t myproject-customer-service .
$ docker tag myproject-customer-service:latest 222337787619.dkr.ecr.ap-southeast-2.amazonaws.com/myproject-customer-service:latest
$ docker run -d -p 5000:5000 myproject-customer-service:latest
```

- Test using curl scripts ~/environment/myproject-customer-service/curl_scripts.md

- Push our Docker Image to ECR and validate
```bash
$ $(aws ecr get-login --no-include-email)
$ docker push 222337787619.dkr.ecr.ap-southeast-2.amazonaws.com/myproject-customer-service:latest
$ aws ecr describe-images --repository-name myproject-customer-service
```

- Add Buildspec Yaml file ~/environment/myproject-customer-service/buildspec.yml

## Manual Deployment
- Create ELB Service Role if it doesnt exist yet
```
$ aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing" || aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"
```

- Add Kubernetes Deployment and Service Yaml files ~/environment/myproject-customer-service/kubernetes/deployment.yml and ~/environment/myproject-customer-service/kubernetes/service.yml

- Create k8s Deployment and Service
```
$ cd ~/environment/myproject-customer-service/kubernetes
$ kubectl apply -f deployment.yml
$ kubectl apply -f service.yml
$ kubectl get deployment myproject-customer-service
```

- Scale the service
```
$ kubectl get deployments
$ kubectl scale deployment myproject-customer-service --replicas=2
$ kubectl get deployments
```

- Find the Service Address
```
$ kubectl get service myproject-customer-service -o wide
```

- Test using curl scripts ~/environment/myproject-customer-service/curl_scripts.md

## Automatic Deployment
- Make changes, commit and push changes to CodeCommit repository to trigger codepipeline deployment to EKS
```bash
$ git add .
$ git commit -m "Initial Commit"
$ git push origin master
```

- Test using curl scripts ~/environment/myproject-customer-service/curl_scripts.md

## (Optional) Clean up
```bash
$ kubectl delete -f service.yml
$ kubectl delete -f deployment.yml
$ aws ecr delete-repository --repository-name myproject-customer-service --force
$ aws codecommit delete-repository --repository-name myproject-customer-service
$ rm -rf ~/environment/myproject-customer-service
$ docker ps
$ docker kill < ad04385ef6dc >
$ docker system prune -a
```