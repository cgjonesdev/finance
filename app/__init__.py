import os
from config import Config
split_path = os.getcwd().split(os.sep)
os.chdir(os.sep.join(split_path[:split_path.index('app') + 1]))
cfg = Config('configs/app.cfg')
