import time
import requests
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# URL of the liveness endpoint
LIVENESS_URL = "http://localhost:30000/health/liveness"
KUBE_HEALTH_CHECK_CMD = "kubectl cluster-info"


# Function to check the liveness of the application
def check_liveness():
    try:
        response = requests.get(LIVENESS_URL)
        if response.status_code == 200:
            logging.info("Liveness check passed: Application is healthy.")
        else:
            logging.warning(
                f"Liveness check failed with status code {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        logging.error(f"Error checking liveness endpoint: {e}")


# Function to check the Kubernetes cluster health
def check_kube_health():
    try:
        result = subprocess.run(
            KUBE_HEALTH_CHECK_CMD, shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            logging.info("Kubernetes cluster is healthy.")
        else:
            logging.warning("Kubernetes cluster check failed.")
            logging.warning(f"Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Error checking Kubernetes cluster health: {e}")


# Periodic check loop
def periodic_health_check(interval=60):
    while True:
        logging.info("Performing health checks...")

        # Check liveness endpoint
        check_liveness()

        # Check Kubernetes cluster health
        check_kube_health()

        # Wait for the next check
        logging.info(f"Waiting for {interval} seconds before the next check...")
        time.sleep(interval)


if __name__ == "__main__":
    # Run the health check every 60 seconds
    periodic_health_check(interval=5)
