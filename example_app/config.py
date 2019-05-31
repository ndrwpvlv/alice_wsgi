import os


class Config:
    TEMPLATES_PATH = '{}/templates/'.format(os.path.dirname(os.path.abspath(__file__)))
    STATIC_PATH = '{}/static/'.format(os.path.dirname(os.path.abspath(__file__)))
