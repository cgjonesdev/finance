import re
from datetime import datetime
from bson import ObjectId
from finance.app.config import Config
from finance.app.logger import logger
cfg = Config('configs/app.cfg')


class Form(object):

    def __init__(self, field_type):
        self.fields = dict(f.split(':') for f in cfg[field_type].split(','))

    def process(self, form_data):
        logger.debug('form_data: {}, self.fields: {}'.format(form_data, self.fields))
        for k, v in form_data.items():
            for field in self.fields:
                sub = re.sub('{}'.format(''.join(k.split(field))), '', k)
                if field == k:
                    if v == '' and self.fields[field] == 'float':
                        continue
                    if k == 'date':
                        v = v.split
                        logger.debug(v)
                    exec('self.__dict__[k] = {}(v)'.format(self.fields[field]))
                elif sub == '_id' and k != 'user_id' and self.fields[field] == 'ObjectId':
                    try:
                        ObjectId(v)
                        exec('self.__dict__[\'{}\'] = {}(v)'.format(
                            sub, self.fields[field]))
                    except:
                        continue
                elif sub == field and sub != '_id':
                    if v == '' and self.fields[field] == 'float':
                        continue
                    exec('self.__dict__[\'{}\'] = {}(v)'.format(
                        sub, self.fields[field]))
        return {k: v for k, v in self.__dict__.items() if k != 'fields'}

    def to_obj(self, form_data, klass):
        data = self.process(form_data)
        obj = type(str(klass), (klass.__mro__[1],), data)
        return obj
