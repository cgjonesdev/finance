from ConfigParser import ConfigParser


class Config(ConfigParser):

    def __init__(self, files, *args, **kwargs):
        ConfigParser.__init__(self, *args, **kwargs)
        self.read(files, *args, **kwargs)

    def __iter__(self):
        items = []
        for section in self.sections():
            items.append((section, dict(self.items(section))))
        return (x for x in items)

    def __getitem__(self, key):
        for section in self.sections():
            for option in self.options(section):
                if option == key.lower():
                    return self.get(section, option)

    def __setitem__(self, key, value):
        for section in self.sections():
            for option in self.options(section):
                print option, key.lower()
                if option == key.lower():
                    self.set(section, option, value)



if __name__ == '__main__':
    cfg = config('app.cfg')
    cfg['TEST'] = 'alsdjfkalsdjfk'
    print list(cfg)
