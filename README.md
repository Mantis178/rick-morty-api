# Rick and Morty Character API Service

This service provides filtered information about characters from the Rick and Morty TV show. It specifically returns data about human characters who are alive and originate from Earth.

## Project Structure

```
rickmorty-service/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
└── yamls/            # Kubernetes manifests
    ├── deployment.yaml
    ├── service.yaml
    └── ingress.yaml
```

## Building and Running with Docker

To build and run the Docker image locally:

1. Build the Docker image:
   ```bash
   docker build -t rickmorty-api .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 rickmorty-api
   ```

The service will be available at `http://localhost:5000`

## API Endpoints

The service provides the following REST API endpoints:

1. Get Characters (JSON):
   ```
   GET /characters
   ```
   Returns filtered character data in JSON format.
   
   Example response:
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

2. Get Characters (CSV):
   ```
   GET /characters/csv
   ```
   Returns the same data in CSV format as a downloadable file.

3. Health Check:
   ```
   GET /healthcheck
   ```
   Returns service health status including Rick and Morty API availability.
   
   Example response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2024-02-02T14:30:45.123456",
     "checks": {
       "rick_and_morty_api": {
         "status": "healthy",
         "latency_ms": 245.67,
         "status_code": 200
       }
     }
   }
   ```

## Deploying to Kubernetes

Prerequisites:
- Minikube installed and running
- kubectl configured
- Ingress addon enabled

Steps to deploy:

1. Start Minikube:
   ```bash
   minikube start
   ```

2. Enable Ingress addon:
   ```bash
   minikube addons enable ingress
   ```

3. Build and load the Docker image into Minikube:
   ```bash
   docker build -t rickmorty-api .
   minikube image load rickmorty-api:latest
   ```

4. Apply Kubernetes manifests:
   ```bash
   kubectl apply -f yamls/
   ```

5. Verify deployment:
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get ingress
   ```

To access the service:
```bash
minikube ip    # Get the Minikube IP address
```
Then add the IP address to your hosts file or access directly using the IP.

## Running Tests

You can test the endpoints using curl:

```bash
# Health check
curl http://localhost:5000/healthcheck

# Get character data in JSON
curl http://localhost:5000/characters

# Download CSV file
curl http://localhost:5000/characters/csv > characters.csv
```

## Helm Chart Deployment

[This section will be added when we create the Helm chart]

## GitHub Actions Workflow

[This section will be added when we create the GitHub Actions workflow]