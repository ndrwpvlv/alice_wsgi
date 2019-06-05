# -*- coding: utf-8 -*-

import os

from alice_wsgi.environment import MIME_TYPES_MAP, ALPHANUM_PATTERN


def binary_string(s: any) -> bin:
    return s.encode('utf-8') if isinstance(s, str) else s


def get_file_extension(path: str):
    return os.path.splitext(path)[1]


def get_mime(extension: str) -> str:
    mime_type = MIME_TYPES_MAP.get('.{}'.format(string_restrip(extension, ALPHANUM_PATTERN))) or 'text/html'
    return mime_type


def wraps_func(func, decorators: list):
    """
    Wrap functions with n-decorators
    :param func: function to wrap
    :param decorators: list of decorators
    :return: decorated function
    """
    if len(decorators) > 0:
        for decorator in decorators:
            func = decorator(func)
    return func


def string_restrip(s: str, regex_compiled) -> str:
    return regex_compiled.sub('', str(s))


def flatten_list(l: list or tuple) -> list:
    return [item for sublist in list(l) for item in sublist]


def format_value(value: str) -> any:
    return int(float(value)) if value.isdigit() else float(value) if value.replace('.', '', 1).isdigit() else value


def path_split(path: str) -> list:
    return [item.replace(' ', '') for item in path.split('/') if item]
