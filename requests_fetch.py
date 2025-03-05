import logging
import requests
import time

from db import log_to_db
from functions import log_message
from constans import urls

LOG_FILE = "req_logs.txt"

logging.basicConfig(
    filename="req_logs_logging.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def fetch_content(url):
    start_time = time.time()
    log_message(LOG_FILE, f"Запит до {url} розпочато")
    logging.info(f"Request to {url} started")
    try:
        response = requests.get(url)
        status = response.status_code
        log_message(LOG_FILE, f"Відповідь для {url} отримано зі статусом {status}")
        logging.info(f"Response for {url} received with status {status}")
        end_time = time.time() - start_time
        return status, round(end_time, 2)
    except Exception as e:
        log_message(LOG_FILE, f"Помилка при запиті до {url}: {e}")
        logging.error(f"Error requesting {url}: {e}")

def main():
    for url in urls:
        result = fetch_content(url)
        if result:
            log_to_db(url, result[0], 'requests', result[1])

if __name__ == "__main__":
    main()
