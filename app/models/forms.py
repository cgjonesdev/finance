import re
from bson import ObjectId
from finance.app.config import Config
from finance.app.logger import logger
cfg = Config('configs/app.cfg')


class Form(object):

    def __init__(self, field_type):
        self.fields = dict(f.split(':') for f in cfg[field_type].split(','))

    def process(self, form_data):
        for k, v in form_data.items():
            for field in self.fields:                
                sub = re.sub('{}'.format(''.join(k.split(field))), '', k)
                if field == k:
                    exec('self.__dict__[k] = {}(v)'.format(self.fields[field]))
                elif sub == '_id' and k != 'user_id' and self.fields[field] == 'ObjectId':
                    try:
                        ObjectId(v)
                        exec('self.__dict__[\'{}\'] = {}(v)'.format(
                            sub, self.fields[field]))
                    except:
                        continue
                elif sub == field and sub != '_id':
                    exec('self.__dict__[\'{}\'] = {}(v)'.format(
                        sub, self.fields[field]))
        return {k: v for k, v in self.__dict__.items() if k != 'fields'}

    def to_obj(self, form_data, klass):
        data = self.process(form_data)
        obj = type(str(klass), (klass.__mro__[1],), data)
        return obj
