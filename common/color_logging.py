import logging
import colorlog

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

class SqlFilter(logging.Filter):
    def filter(self, record):
        # record.args[0] содержит SQL-запрос
        sql = getattr(record, 'sql', None)
        if sql is None and hasattr(record, 'getMessage'):
            sql = record.getMessage()
        if not sql:
            return False
        sql_upper = sql.strip().upper()
        # Логируем только нужные запросы
        return (
            sql_upper.startswith("INSERT") or
            sql_upper.startswith("UPDATE") or
            sql_upper.startswith("DELETE")
        )

# Форматтер для aiogram
aiogram_handler = colorlog.StreamHandler()
aiogram_handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s[AIROGRAM] %(asctime)s | %(levelname)s | %(message)s",
    log_colors={
        'DEBUG':    'yellow',
        'INFO':     'yellow',
        'WARNING':  'yellow',
        'ERROR':    'yellow',
        'CRITICAL': 'yellow',
    }
))

# Форматтер для sqlalchemy
sqlalchemy_handler = colorlog.StreamHandler()
sqlalchemy_handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s[SQLALCHEMY] %(asctime)s | %(levelname)s | %(message)s",
    log_colors={
        'DEBUG':    'blue',
        'INFO':     'blue',
        'WARNING':  'blue',
        'ERROR':    'blue',
        'CRITICAL': 'blue',
    }
))

# Форматтер для всего остального — зелёный
default_handler = colorlog.StreamHandler()
default_handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s[DEFAULT] %(asctime)s | %(levelname)s | %(message)s",
    log_colors={
        'DEBUG':    'green',
        'INFO':     'green',
        'WARNING':  'green',
        'ERROR':    'green',
        'CRITICAL': 'green',
    }
))

# Отключаем все дефолтные обработчики
for logger_name in ('aiogram', 'sqlalchemy.engine.Engine', ''):
    logging.getLogger(logger_name).handlers.clear()

# Настраиваем aiogram
aiogram_logger = logging.getLogger("aiogram")
aiogram_logger.setLevel(logging.INFO)
aiogram_logger.addHandler(aiogram_handler)
aiogram_logger.propagate = False

# Настраиваем sqlalchemy
sql_logger = logging.getLogger("sqlalchemy.engine.Engine")
sql_logger.setLevel(logging.INFO)
sql_logger.addHandler(sqlalchemy_handler)
sql_logger.propagate = False

# Настраиваем корневой логгер
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(default_handler)