import time
import logging
import random
from prometheus_client import start_http_server, Counter

# Configuration Prometheus
ERROR_COUNTER = Counter('app_requests_errors_total', 'Total error count', ['app_name', 'endpoint'])

# Configuration Logging (pour Loki via Promtail ou Docker)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] app=my-python-app endpoint=%(endpoint)s message=%(message)s'
)

def simulate_traffic():
    endpoints = ['/api/v1/user', '/api/v1/order', '/api/v1/payment']
    while True:
        endpoint = random.choice(endpoints)

        # Simulation d'une erreur (20% de chance)
        if random.random() < 0.2:
            logging.error(f"Failed to process request", extra={'endpoint': endpoint})
            ERROR_COUNTER.labels(app_name='my-python-app', endpoint=endpoint).inc()
        else:
            logging.info(f"Successful request", extra={'endpoint': endpoint})

        time.sleep(random.uniform(1, 5))

if __name__ == "__main__":
    start_http_server(8000)
    print("Application démarrée sur le port 32550...")
    simulate_traffic()