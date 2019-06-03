# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, FileSystemLoader

from alice_wsgi.helpers import binary_string
from alice_wsgi.request import Request
from alice_wsgi.routes import Router


class Alice:
    """
    Base class for Alice_WSGI framework
    """

    def __init__(self, config):
        """
        Class has two default handler classes:
        - router as alice_wsgi.routes.Router()
        - jinja as jinja2.Environment for template processing

        :param config: Config from Class with config variables.
                       Required variables config.STATIC_PATH and config.TEMPLATES_PATH
        """
        self.config = config
        self.router = Router(self.config.STATIC_PATH or '{}/static/'.format(os.getcwd()), )
        self.jinja = Environment(loader=FileSystemLoader(self.config.TEMPLATES_PATH))
        self.start_response = None

    def __call__(self, environ: dict, start_response):
        """
        Work in two ways. On response type, extension and mime Alice determine is it file or dynamic request

        :param environ: wsgi environ dict
        :param start_response: wsgi response function
        :return: response status, headers, body or binary file
        """
        self.start_response = start_response
        request = Request(environ).get_request()
        response = self.router.response(request)
        start_response(response['status'], response['headers'])
        return [binary_string(response['body'])]
