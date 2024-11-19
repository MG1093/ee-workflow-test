## Reviewer Instructions
If you are reviewing this submission, then you can do so in two ways

* Look at the changes in [this pull request](https://github.com/equalexperts-assignments/equal-experts-cultured-steadfast-fabulous-phone-b352f4e6ab88/pull/1)
* Browse the code on Github
    



# Equal Experts: Flask GitHub API Gist App

This project provides a Flask web application that interacts with the GitHub API to retrieve public gists for a given user. The app includes support for **pagination** and **caching**, and can be tested using **unit** and **integration tests**.

---

## Overview

You have two options for setting up and running the application:

1. **Manual Setup** – Install dependencies, build the Docker container, and run tests manually.
2. **Automated Pipeline** – Use the provided `local_pipeline.sh` script for a fully automated setup.

---

## Table of Contents

- [Equal Experts: Flask GitHub API Gist App](#equal-experts-flask-github-api-gist-app)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Option 1: Manual Setup](#option-1-manual-setup)
    - [Step 1: Create Virtual Environment \& Install Dependencies](#step-1-create-virtual-environment--install-dependencies)
    - [Step 2: Run Unit Tests](#step-2-run-unit-tests)
    - [Step 3: Build the Docker Image](#step-3-build-the-docker-image)
    - [Step 4: Start the Docker Container](#step-4-start-the-docker-container)
    - [Step 5: Run Integration Tests](#step-5-run-integration-tests)
    - [Step 6: Clean Up](#step-6-clean-up)
  - [Option 2: Automated Setup with `local_pipeline.sh` (Dev Only, less dependencies)](#option-2-automated-setup-with-local_pipelinesh-dev-only-less-dependencies)
    - [Step 1: Run the Pipeline Script](#step-1-run-the-pipeline-script)
    - [What the Script Does](#what-the-script-does)
  - [Test Report](#test-report)
    - [Option 3: Run Github Worflow Locally (Enterprise Setup)](#option-3-run-github-worflow-locally-enterprise-setup)
  - [BUG: To be fixed](#bug-to-be-fixed)
  - [Requirements](#requirements)
  - [Notes](#notes)

---

## Option 1: Manual Setup

### Step 1: Create Virtual Environment & Install Dependencies

1. **Create a Virtual Environment**:

   ```bash
   python3.12 -m venv .venv
   ```

2. **Activate the Virtual Environment**:

   ```bash
   source .venv/bin/activate
   ```

3. **Install Required Dependencies**:

   ```bash
   pip install -r app/requirements.txt
   pip install -r tests/requirements.txt
   ```

---

### Step 2: Run Unit Tests

Run the unit tests to ensure everything works locally:

```bash
pytest -vv tests/unit_tests --maxfail=1
```

---

### Step 3: Build the Docker Image

Once the unit tests pass, build the Docker image:

```bash
docker build -t equal-exports-gist-app-img .
```

---

### Step 4: Start the Docker Container

Run the Docker container on port `8080`:

```bash
docker run -d --name equal-exports-gist-app -p 8080:8080 equal-exports-gist-app-img
```

---

### Step 5: Run Integration Tests

Run the integration tests against the running Docker container:

```bash
pytest -vv tests/integration_tests/test_main.py --maxfail=1
```

---

### Step 6: Clean Up

After tests are finished, stop and remove the Docker container:

```bash
docker stop equal-exports-gist-app
docker rm equal-exports-gist-app
```

---

## Option 2: Automated Setup with `local_pipeline.sh` (Dev Only, less dependencies)

For a fully automated process, use the `local_pipeline.sh` script. This script will handle everything from dependency installation to running tests and managing Docker.

### Step 1: Run the Pipeline Script

Make sure the script is executable and then run it:

```bash
chmod +x local_pipeline.sh  # Make it executable
./local_pipeline.sh         # Run the script
```

### What the Script Does

- Creates and activates a virtual environment
- Installs dependencies from `requirements.txt`
- Runs unit tests
- Pip install and docker logs are directed to log files
- Generates an HTML report of the test results and coverage
- Builds the Docker container if unit tests pass
- Starts the Docker container and runs integration tests
- Cleans up by stopping and removing the Docker container

---

## Test Report

The `local_pipeline.sh` script will generate an HTML test report located in the `tests/coverage_html_report` directory. Open this file in a browser to view detailed test results and coverage information.

---

### Option 3: Run Github Worflow Locally (Enterprise Setup)

To run the CI/CD pipeline locally, ensure the following prerequisites are met:

Docker Desktop is installed, with Kubernetes enabled.

The act CLI is installed. Follow the installation guide here: https://nektosact.com/installation/index.html.

If you want to run the CI Pipeline locally

```bash
act pull_request --graph
act pull_request -e event.json
```

If you want to run the CD pipeline locally

## BUG: To be fixed

For now run these commands after the CI pipeline, incorporating this into CD locally still WIP

```bash
kubectl apply -f k8s/deployments.yaml  
kubectl apply -f k8s/services.yaml  
```

```bash
act release --graph
act release -e event.json -s KUBECONFIG_CONTENT="$(~/.kube/config)"
```


## Requirements

- **Python 3.12** or higher
- **Docker**
- **pip** (for installing Python dependencies)
- **pytest** (for running the tests)

---

## Notes

- **Manual Setup**: If you choose to manually set up the app, make sure to start the Docker container and run tests separately.
- **Automated Setup**: The `local_pipeline.sh` script automates all steps, including setting up the environment, installing dependencies, running tests, and handling Docker.
- **Local Development**: If you prefer local development without using Docker, you can run the Flask app directly by executing:

  ```bash
  python3 app/main.py
  ```