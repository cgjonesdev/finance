import logging


FORMAT = ('%(levelname)-8s %(filename)s:%(lineno)d:%(funcName)s '
		  '|%(message)s| %(asctime)s')
logging.basicConfig(format=FORMAT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)