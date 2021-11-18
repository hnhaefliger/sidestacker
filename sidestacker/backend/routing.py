from django.urls.resolvers import RoutePattern
from .connection import Connection


class Router:
    def __init__(self, url, application):
        self.pattern = RoutePattern(url)
        self.application = application

    def __call__(self, scope, receive, send):
        match = self.pattern.match(scope['path'])

        if match != None:
            return Connection(scope, receive, send, self.application, **match[2])

        else:
            return False


def socket_path(url, application):
    return Router(url, application)
