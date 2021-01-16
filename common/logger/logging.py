import logging
from logging.handlers import RotatingFileHandler


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt="%d-%m-%Y %H:%M:%S",
    filename='logs.txt',

)

logger = logging.getLogger("jobJournal")
handler = RotatingFileHandler('logs.txt', maxBytes=1000, backupCount=4)
handler.setLevel(logging.WARNING)
logger.addHandler(handler)