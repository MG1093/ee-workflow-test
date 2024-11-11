#!/bin/bash

# Define variables
VENV_DIR=".venv"
REQUIREMENTS_FILE="app/requirements.txt"
TESTS_REQUIREMENTS_FILE="tests/requirements.txt"
DOCKER_IMAGE_NAME="equal-exports-gist-app-img"
DOCKER_CONTAINER_NAME="equal-exports-gist-app"
INTEGRATION_TEST_SCRIPT="tests/integration_tests/test_main.py"
COVERAGE_HTML_REPORT="coverage_report.html"

# Create virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "### Step 1: Virtual environment already exists. Skipping creation. ###"
else
    python3.12 -m venv $VENV_DIR
    echo "### Step 1: Virtual environment created in .venv ###"
fi

echo "### Step 2: Activating virtual environment ###"
source $VENV_DIR/bin/activate

# Ensure requirements.txt exists before attempting to install
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Error: $REQUIREMENTS_FILE not found. Exiting."
    exit 1
fi

echo "### Step 3: Installing Requirements.txt ###"
pip install --upgrade pip > /dev/null 2>> pip_install.log
pip install -r $REQUIREMENTS_FILE > /dev/null 2>> pip_install.log
pip install -r $TESTS_REQUIREMENTS_FILE > /dev/null 2>> pip_install.log

echo "### Step 4: Run unit tests with coverage ###"
coverage run -m pytest tests/unit_tests --maxfail=1 -v

# Check if unit tests passed
if [ $? -ne 0 ]; then
    echo "Unit tests failed. Exiting."
    deactivate
    exit 1
fi

echo "### Step 5: Display coverage report in terminal ###"
coverage report  # Display coverage in terminal

echo "### Step 6: Generate HTML coverage report ###"
coverage html -d $COVERAGE_HTML_REPORT  # Generate HTML coverage report

# Check if the HTML report was generated successfully
if [ ! -d $COVERAGE_HTML_REPORT ]; then
    echo "Error: HTML coverage report generation failed. Exiting."
    deactivate
    exit 1
fi

# Step 7: Build Docker image after unit tests passed
echo "### Step 7: Building Docker image ###"
docker build -t $DOCKER_IMAGE_NAME . > /dev/null 2>> docker_build.log

echo "### Step 8: Starting Docker container ###"
docker run -d --name $DOCKER_CONTAINER_NAME -p 8080:8080 $DOCKER_IMAGE_NAME

echo "### Step 9: Running Integration Tests against container ###"
coverage run -m pytest $INTEGRATION_TEST_SCRIPT --maxfail=1 -v

# Check if integration tests passed
if [ $? -ne 0 ]; then
    echo "Integration tests failed. Stopping the Docker container."
    docker stop $DOCKER_CONTAINER_NAME . > /dev/null 2>> docker_remove.log
    docker rm $DOCKER_CONTAINER_NAME . > /dev/null 2>> docker_remove.log
    deactivate
    exit 1
fi

# Step 12: Clean up Docker container
echo "### Step 10: Clean up Docker container ###"
docker stop $DOCKER_CONTAINER_NAME . > /dev/null 2>> docker_remove.log
docker rm $DOCKER_CONTAINER_NAME . > /dev/null 2>> docker_remove.log

# Deactivate virtual environment
deactivate

echo "### SUCCESS: Setup, testing, and cleanup completed successfully! ###"
