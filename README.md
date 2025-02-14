# Rick and Morty Character API Service

A service that interacts with the Rick and Morty API to filter and serve character information. The service specifically returns human characters who are alive and originate from Earth.

## Table of Contents
- [Project Structure](#project-structure)
- [Base Application](#base-application)
  - [Flask API Service](#flask-api-service)
  - [API Endpoints](#api-endpoints)
  - [Local Development](#local-development)
- [Docker Implementation](#docker-implementation)
  - [Building the Image](#building-the-image)
  - [Running the Container](#running-the-container)
  - [Docker Configuration](#docker-configuration)
- [Kubernetes Deployment](#kubernetes-deployment)
  - [Prerequisites](#kubernetes-prerequisites)
  - [Deployment Files](#deployment-files)
  - [Deploying with kubectl](#deploying-with-kubectl)
  - [Accessing the Service](#accessing-the-service)
- [Helm Chart](#helm-chart)
  - [Chart Structure](#chart-structure)
  - [Configuration Options](#configuration-options)
  - [Installation and Upgrades](#installation-and-upgrades)
  - [Troubleshooting](#helm-troubleshooting)
- [GitHub Actions CI/CD](#github-actions-cicd)
  - [Workflow Structure](#workflow-structure)
  - [Monitoring and Debugging](#monitoring-and-debugging)
  - [Customization](#workflow-customization)

## Project Structure
```
project-root/
├── app.py                     # Flask application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── helm/                      # Helm chart directory
│   └── rickmorty/        
│       ├── Chart.yaml         # Chart metadata
│       ├── values.yaml        # Default configuration
│       └── templates/         # Kubernetes template files
│           ├── deployment.yaml
│           ├── service.yaml
│           └── ingress.yaml
├── .github/
│   └── workflows/            # GitHub Actions workflows
│       └── deploy.yaml       # CI/CD pipeline definition
└── yamls/                    # Direct Kubernetes manifests
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

## Base Application

### Flask API Service
The core service is built using Flask and provides endpoints to:
- Fetch and filter Rick and Morty characters
- Return data in both JSON and CSV formats
- Monitor service health

Dependencies:
```
flask==2.0.1
werkzeug==2.0.3
requests==2.26.0
gunicorn==20.1.0
```

### API Endpoints

1. Get Characters (JSON):
```bash
GET /characters
```
Response:
```json
{
    "status": "success",
    "count": 5,
    "data": [
        {
            "Name": "Rick Sanchez",
            "Origin": "Earth",
            "Location": "Earth",
            "Image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg"
        }
    ]
}
```

2. Download CSV:
```bash
GET /characters/csv
```
Returns: CSV file with columns Name, Origin, Location, Image

3. Health Check:
```bash
GET /healthcheck
```
Response:
```json
{
    "status": "healthy",
    "timestamp": "2024-02-14T12:00:00Z",
    "checks": {
        "rick_and_morty_api": {
            "status": "healthy",
            "latency_ms": 245.67
        }
    }
}
```

### Local Development
1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Docker Implementation

### Building the Image
Build with:
```bash
docker build -t rickmorty-api:latest .
```

The Dockerfile:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Running the Container
Run locally:
```bash
docker run -p 5000:5000 rickmorty-api:latest
```

Verify:
```bash
curl http://localhost:5000/healthcheck
```

### Docker Configuration
The container:
- Uses Python 3.9 slim base image for smaller size
- Runs on port 5000
- Uses gunicorn for production deployment
- Includes health check capabilities

## Kubernetes Deployment

### Kubernetes Prerequisites
1. Minikube installed and running:
```bash
minikube start
```

2. kubectl configured:
```bash
kubectl config use-context minikube
```

### Deployment Files
Three main Kubernetes manifests in `yamls/`:

1. deployment.yaml:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rickmorty-api
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: rickmorty-api
          image: rickmorty-api:latest
          ports:
            - containerPort: 5000
```

2. service.yaml:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: rickmorty-api
spec:
  ports:
    - port: 80
      targetPort: 5000
```

3. ingress.yaml (configured for basic HTTP routing)

### Deploying with kubectl
1. Build and load image into minikube:
```bash
minikube image build -t rickmorty-api:latest .
```

2. Apply manifests:
```bash
kubectl apply -f yamls/
```

3. Verify deployment:
```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

### Accessing the Service
1. Port forwarding:
```bash
kubectl port-forward service/rickmorty-api 8080:80
```

2. Minikube IP (with Ingress):
```bash
minikube ip
# Access via http://MINIKUBE_IP
```

## Helm Chart

### Chart Structure
```
helm/rickmorty/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
└── templates/          # Template files
```

Important settings in values.yaml:
```yaml
replicaCount: 2
image:
  repository: rickmorty-api
  tag: latest
  pullPolicy: Never
service:
  type: ClusterIP
  port: 80
```

### Configuration Options
Full list of configurable parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| replicaCount | Number of replicas | 2 |
| image.repository | Image name | rickmorty-api |
| image.tag | Image tag | latest |
| image.pullPolicy | Pull policy | Never |
| service.type | Service type | ClusterIP |
| service.port | Service port | 80 |
| ingress.enabled | Enable ingress | true |
| resources.limits.cpu | CPU limit | 500m |
| resources.limits.memory | Memory limit | 512Mi |

### Installation and Upgrades
1. Install:
```bash
helm install my-rickmorty ./helm/rickmorty
```

2. Upgrade:
```bash
helm upgrade my-rickmorty ./helm/rickmorty
```

3. Rollback:
```bash
helm rollback my-rickmorty 1
```

4. Uninstall:
```bash
helm uninstall my-rickmorty
```

### Helm Troubleshooting
Common issues and solutions:

1. Image Pull Errors:
```bash
# Check image availability
minikube ssh 'docker images'
```

2. Pod Startup Issues:
```bash
# Check pod status
kubectl describe pod [POD_NAME]
```

3. Service Connection Issues:
```bash
# Verify service
kubectl get endpoints
```

## GitHub Actions CI/CD

### Workflow Structure
The workflow in `.github/workflows/deploy.yaml` contains:

1. Triggers:
```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

2. Environment Setup:
- Python 3.9
- Minikube
- Helm
- Docker

3. Build and Test Sequence:
- Build Docker image
- Deploy to Minikube
- Run integration tests
- Cleanup resources

### Monitoring and Debugging
1. View workflow runs:
- Go to GitHub repository
- Click "Actions" tab
- Select workflow run

2. Debug information available:
- Container logs
- Pod status
- Test results
- Deployment events

3. Common status checks:
```bash
# Pod status
kubectl get pods
# Service status
kubectl get services
# Events
kubectl get events
```

### Workflow Customization
Customize the workflow by modifying:
1. Trigger conditions in `on:` section
2. Resource limits in deployment
3. Test parameters
4. Timeout values

Example of adding custom test:
```yaml
- name: Custom Test
  run: |
    response=$(curl -s http://localhost:8080/characters)
    echo $response | jq .count
```

For detailed test results, check the Actions tab after each workflow run.