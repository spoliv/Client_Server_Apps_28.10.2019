import sys
import os
import logging
from HomeWorks.Lesson_4.common.constants import LOGGING_LEVEL
sys.path.append('../')


# Создаём формировщик логов (formatter):

client_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path_to_log = os.path.join(path, 'logfiles', 'client.log')

# создаём потоки вывода логов
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(client_formatter)
steam.setLevel(logging.ERROR)
log_file = logging.FileHandler(path_to_log, encoding='utf8')
log_file.setFormatter(client_formatter)

# создаём регистратор и настраиваем его
logger = logging.getLogger('client')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    logger.critical('Test critical event')
    logger.error('Test error ivent')
    logger.debug('Test debug ivent')
    logger.info('Test info ivent')
