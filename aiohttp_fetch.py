# Завдання 1
# Створіть співпрограму, яка отримує контент із зазначених посилань і логує хід виконання в database, використовуючи
# стандартну бібліотеку requests, а потім проробіть те саме з бібліотекою aiohttp. Кроки, які мають бути залоговані:
# початок запиту до адреси X, відповідь для адреси X отримано зі статусом 200. Перевірте хід виконання програми на >3
# ресурсах і перегляньте послідовність запису логів в обох варіантах і порівняйте результати. Для двох видів завдань
# використовуйте різні файли для логування, щоби порівняти отриманий результат.

import logging
import time
import aiohttp
import asyncio

from db import log_to_db
from functions import log_message
from constans import urls

LOG_FILE = "async_logs.txt"

logging.basicConfig(
    filename="aio_logs_logging.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

async def fetch_content(session, url):
    start_time = time.time()
    log_message(LOG_FILE, f"Запит до {url} розпочато")
    logging.info(f"Request to {url} started")
    try:
        async with session.get(url) as response:
            status = response.status
            log_message(LOG_FILE, f"Відповідь для {url} отримано зі статусом {status}")
            logging.info(f"Response for {url} received with status {status}")
            end_time = time.time() - start_time
            return url, status, end_time
    except Exception as e:
        log_message(LOG_FILE, f"Помилка при запиті до {url}: {e}")
        logging.error(f"Error requesting {url}: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_content(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

if __name__ == "__main__":
    results = asyncio.run(main())

    if results:
        for url, status, end_time in results:
            if status is not None:
                log_to_db(url, status, 'aiohttp', round(end_time, 2))
