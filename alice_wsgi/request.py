import urllib.parse as urlparse

from .environment import METHODS_ALLOWED_GLOBAL
from .helpers import get_mime, get_file_extension


class Request:
    def __init__(self, environ):
        """
        Basic request processing class
        :param environ: WSGI environ
        """
        self.environ = environ
        self.path = self.environ.get('PATH_INFO')
        self.method = self.environ.get('REQUEST_METHOD') if self.environ.get(
            'REQUEST_METHOD') in METHODS_ALLOWED_GLOBAL else METHODS_ALLOWED_GLOBAL[0]
        self.query = self.query_variables(
            self.environ.get('QUERY_STRING')) if self.method == 'GET' else self.post_query_variables()
        self.file_extension = get_file_extension(self.path) or None
        self.mime = environ.get('HTTP_ACCEPT').split(',')[0] if environ.get('HTTP_ACCEPT') else get_mime(
            self.file_extension)

    @staticmethod
    def query_variables(query):
        """
        Parse query variables
        :param query: GET or POST query variables parse
        :return: dict with variables
        """
        return urlparse.parse_qs(query) if query else {}

    def post_query_variables(self):
        """
        Get POST query variables
        :return: dict with variables
        """
        try:
            request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0
        query = self.environ['wsgi.input'].read(request_body_size).decode('utf-8')
        return self.query_variables(query)

    def get_request(self):
        """
        Parsed request to dict {path:, method:, mime:, query:, extension: file extension, }
        :return: dict
        """
        return {
            'path': self.path,
            'method': self.method,
            'mime': self.mime,
            'query': self.query,
            'extension': self.file_extension,
        }
