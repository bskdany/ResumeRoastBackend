# Resume Wrecker API

## Overview

The **Resume Roast API** is a Flask-based web application designed to provide humorous and constructive feedback on resumes. Users can upload their resumes, specify their job title and desired feedback intensity (tolerance level), and receive an audio "roast" of their resume. The feedback is generated using OpenAI's GPT model and converted to speech using Azure Cognitive Services.

The application is containerized using Docker and can be deployed to Azure using Terraform. It integrates with Azure Blob Storage for resume storage and Azure Cosmos DB for metadata storage.

---

## Features

- **Resume Upload**: Users can upload their resumes via a form.
- **Feedback Generation**: OpenAI's GPT model generates feedback based on the resume content, job title, and tolerance level.
- **Text-to-Speech**: Azure Cognitive Services converts the feedback into speech.
- **Task Queue**: A queue system ensures feedback requests are processed in order.
- **Health Check**: A `/healthz` endpoint monitors the application's status.
- **CORS Support**: Cross-Origin Resource Sharing (CORS) is enabled for frontend integration.

---

## Technologies Used

- **Flask**: Python web framework for building the API.
- **Docker**: Containerization for packaging the application.
- **Azure Blob Storage**: Stores uploaded resumes.
- **Azure Cosmos DB**: Stores metadata about resume submissions.
- **Azure Cognitive Services**: Handles text-to-speech conversion.
- **Deepseek AI**: Generates feedback based on resume content.
- **Terraform**: Infrastructure as Code (IaC) for Azure deployment.
- **GitHub Actions**: CI/CD pipelines for building and deploying the application.

---

## Getting Started

### Prerequisites

- Docker
- Python 3.12
- Azure account with necessary permissions
- Terraform
- Azure CLI (to run terraform locally)
- Deepseek API key
- Azure Cognitive Services API key

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/resume-roast-api.git
   cd resume-roast-api
   ```
2. **Set up environment variables**
```
ACCOUNT=<Azure Blob Storage Account>
KEY=<Azure Blob Storage Key>
CONTAINER=<Azure Blob Storage Container>
COSMOS_ENDPOINT=<Azure Cosmos DB Endpoint>
COSMOS_KEY=<Azure Cosmos DB Key>
COSMOS_DATABASE_NAME=<Azure Cosmos DB Database Name>
COSMOS_CONTAINER_NAME=<Azure Cosmos DB Container Name>
AZURE_STORAGE_CONNECTION_STRING=<Azure Storage Connection String>
ELEVEN_API_KEY=<ElevenLabs API Key>
SPEECH_API_KEY=<Azure Speech API Key>
SPEECH_ENDPOINT=<Azure Speech Endpoint>
SPEECH_REGION=<Azure Speech Region>
OPENAI_KEY=<OpenAI API Key>
```
3. **Build and run in Docker container**
```bash
docker-compose up --build
``` 
4. Access the application
The application will be available at `http://localhost:8080`.

### Deployment Azure
1. Set up Terraform:
Ensure Terraform is installed and configured with your Azure credentials.
2. Initialize Terraform:
```bash
cd Terraform
terraform init
```
3. Apply Terraform configuration:
```bash
terraform apply
```
4. Deploy using GitHub Actions:
Push changes to the main branch to trigger the GitHub Actions workflow for deployment.
#### API Endpoints
- **POST /form:** Submit a resume and receive feedback.
- G**ET /add-audio:** Add a task to the queue for audio generation.
- **GET /get-audio:** Retrieve the generated audio feedback.
- **GET /healthz:** Health check endpoint.
