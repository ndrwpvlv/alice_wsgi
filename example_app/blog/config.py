import os

from example_app.config import Config


class Config:
    TEMPLATES_PATH = '{}/templates/'.format(os.path.dirname(os.path.abspath(__file__)))
    STATIC_PATH = Config.STATIC_PATH
