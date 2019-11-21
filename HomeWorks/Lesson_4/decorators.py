import sys
import HomeWorks.Lesson_4.logs.config_server_log
import HomeWorks.Lesson_4.logs.config_client_log
import logging
import inspect

# Определяем, какой logger будет работать

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        logger.debug(
            f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}.'
            f'Вызов из функции {inspect.stack()[1][3]}')
        res = func_to_log(*args, **kwargs)
        return res
    return log_saver
