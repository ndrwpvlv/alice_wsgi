# -*- coding: utf-8 -*-
import itertools
import os
import re

from .environment import HTTP_STATUS_CODES, TYPES_TEMPLATES, VARIABLE_PATTERN
from .helpers import path_split, flatten_list, format_value


class Router:
    def __init__(self, static_path: str):
        """

        :param static_path: Static files path, str
        """
        self.routes = {}  # {PATH: {VIEW_CLS:, METHODS_ALLOWED:, DECORATORS:, }, }
        self.redirects = {}  # {PATH: {REDIRECT_URL:, CODE:,}, }
        self.error_handlers = {}  # {CODE: HANDLER,}
        self.static_path = static_path

    def add_route(self, route: str, view_cls, methods: tuple = ('GET',), decorators: tuple = (), ):
        self.routes[route.replace(' ', '')] = {'view_cls': view_cls, 'methods': methods, 'decorators': decorators,
                                               'pattern': self.pattern_route(route)}

    def add_redirect(self, route: str, redirect_url: str, code: int, ):
        self.redirects[route] = {'redirect_url': redirect_url, 'code': code, }

    def add_error_handler(self, code: int, handler_func):
        self.error_handlers[code] = handler_func

    def get_error_handler(self, code: int, method: str):
        handler = self.error_handlers.get(code)
        return getattr(handler, method.lower()) if handler else http_status

    @staticmethod
    def redirect_handler(redirect_url: str, code: int, ):
        return {'status': http_status(code), 'headers': [('Location', redirect_url)], 'body': http_status}

    @staticmethod
    def pattern_route(
            route: str, variables_patterns: str = VARIABLE_PATTERN, types_templates: dict = TYPES_TEMPLATES, ) -> str:
        """
        Create regex-pattern for route
        :param route: route path with variables pattern
        :param variables_patterns: default pattern for finding variables in path
        :param types_templates: regex-patterns for single types of variables (int, float, str)
        :return: regex-template
        """
        fields = path_split(route)
        return '^/{}/$'.format('/'.join([types_templates.get(t[0][0]) if t[0] else t[1] for t in
                                         [[flatten_list(re.findall(variables_patterns, f)), f] for f in
                                          fields]])).replace('//', '/')

    def get_route(self, path: str) -> dict:
        """
        Get route from Router by path
        :param path: url path in string, str
        :return: dict with route from self.routes and finded formated variables in list
        """
        if path in self.routes:
            route = self.routes.get(path)
            variables = []
        else:
            patterns = {route[1]['pattern']: route[0] for route in self.routes.items()}
            match = self.match_path_patterns(path, list(patterns))
            route = self.routes.get(patterns.get(match[0])) if match else None
            variables = [format_value(v) for v in match[1] if match] if match else []
        return {'route': route,
                'path_variables': variables}

    @staticmethod
    def match_path_patterns(path: str, patterns: list):
        """
        Compare path with list of regex-patterns
        :param path: url path, str
        :param patterns: list of patterns, list
        :return: list with finded pattern and tuple with variables. Example: [pattern_as_str, (var1, var2, )]
        """
        match = [[p, re.findall(p, path)[0]] for p in patterns if re.findall(p, path)]
        match = match[0] if len(match) else None
        if all([isinstance(match[1], str) if match else False]):
            match[1] = tuple() if match[1].startswith('/') else tuple([match[1], ])
        return match

    def find_route(self, request: dict):
        """
        Route finder.
        1) find_route check routes dict.
        2) If in request exists not allowed method return 405
        3) Final return 404

        :param request: dict from Request.get_request
        :return: Redirect, Errors 404 and 405, Response with headers and body.
        """

        route = self.get_route(request['path'])
        if not route.get('route'):
            code = 404
        else:
            if request['method'] in route.get('route').get('methods'):
                code = 200
            else:
                code = 405
        body = getattr(route.get('route').get('view_cls')(), request['method'].lower())(
            *route.get('path_variables'), **request.get('query')) if \
            code == 200 else self.get_error_handler(code, request['method'])(code)

        return self.format_response(body, code, request['mime'])

    @staticmethod
    def get_file(path, request: dict, code: int = 200):
        """
        Get static file
        :param path: path to file
        :param request: request dict
        :param code: http status code
        :return: binary file as body and headers with status
        """
        with open(path, 'rb') as f:
            return {'status': http_status(code), 'headers': [('Content-type', request['mime']), (
                'Content-Length', str(os.path.getsize(path)))], 'body': f.read()}

    @staticmethod
    def format_response(body: str or tuple, code: int = 200, mime: str = 'text/html'):
        """
        Implementation of layer for handle custom http status codes and mimes from Users ClassViews
        :param body: Response body
        :param code: http status code
        :param mime: mime
        :return:
        """
        if isinstance(body, tuple or list):
            substitution = tuple([None, mime, code])
            response = tuple([b[0] or b[1] for b in tuple(itertools.zip_longest(body, substitution))])
        else:
            response = tuple([str(body), str(mime), int(code)])
        return {
            'body': response[0],
            'status': http_status(response[2]),
            'headers': [('Content-type', response[1])],
        }

    def response(self, request):
        path = '{}{}'.format(self.static_path, request['path']).replace('//', '/')
        if request['extension'] and os.path.isfile(path):
            response = self.get_file(path, request)
        elif not request['path'].endswith('/'):
            response = self.redirect_handler('{}/'.format(request['path']), 301)
        elif request['path'] in self.redirects:
            response = self.redirect_handler(self.redirects.get(request['path'])['redirect_url'],
                                             self.redirects.get(request['path'])['code'])
        else:
            response = self.find_route(request)
        return response


def http_status(code: int, http_status_codes: dict = HTTP_STATUS_CODES, template: str = '{} {}'):
    return template.format(code, http_status_codes.get(code) or http_status_codes.get(500))
