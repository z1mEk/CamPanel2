import logging as Logging
from logging.handlers import RotatingFileHandler
from general.configLoader import config

log_formatter = Logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler(filename=config.logger.fileName, maxBytes=config.logger.maxBytes, backupCount=config.logger.backupCount)
log_handler.setFormatter(log_formatter)
logger = Logging.getLogger()
logger.setLevel(Logging.INFO)
logger.addHandler(log_handler)
logging = Logging