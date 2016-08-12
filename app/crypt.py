import hmac
from config import Config
from logger import logger

cfg = Config('configs/app.cfg')


def make_digest(*args):
    digest_maker = hmac.new(cfg['SECRET_KEY'])
    for arg in args:
        digest_maker.update(arg)
    return digest_maker.hexdigest()

def validate_digest(a, b):
    return a == b
