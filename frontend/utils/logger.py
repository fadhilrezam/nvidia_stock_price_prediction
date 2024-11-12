import logging
from datetime import datetime
import os

logs_path = os.path.join(os.path.dirname(__file__),"..","logs")
os.makedirs(logs_path, exist_ok=True)

log_file_name = f'{datetime.now().strftime("%Y-%m-%d")}.log'
log_file_path = os.path.abspath(os.path.join(logs_path, log_file_name))

logging.basicConfig(
    filename = log_file_path,
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    logging.info('Logging has started')
    logging.info(f'Log File sucessfully created in {log_file_path}')
