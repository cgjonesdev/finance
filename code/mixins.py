import json
from lib.mixins import Magic


class IO(object):

    def read(self):
        with open(self.filename) as _:
            self.data = json.loads(_.read())

    def write(self):
        with open(self.filename, 'w') as _:
            _.write(json.dumps(self.data))
