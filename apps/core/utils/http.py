import json

from django.http import HttpResponse
from django.conf import settings


class JSONResponse(HttpResponse):
    def __init__(self, request, data):
        mime = 'application/json'
        content = json.dumps(data)
        super(JSONResponse, self).__init__(content=content, content_type=mime)


class JSONErrorResponse(JSONResponse):
    def __init__(self, request, data):
        super(JSONErrorResponse, self).__init__(request, {'error': data})


class JSONResponseUnauthorized(JSONErrorResponse):
    status_code = 401

    def __init__(self, request, data):
        super(JSONResponseUnauthorized, self).__init__(request, data)
        self['WWW-Authenticate'] = 'Basic realm="%s"' % settings.SITE_NAME


class JSONResponseForbidden(JSONErrorResponse):
    status_code = 403

    def __init__(self, request, data='Forbidden.'):
        super(JSONResponseForbidden, self).__init__(request, data)


class JSONResponseNotFound(JSONErrorResponse):
    status_code = 404


class JSONResponseMethodNotAllowed(JSONErrorResponse):
    status_code = 405

    def __init__(self, request, data=None):
        if not data:
            data = '%s method not allowed.' % request.method
        super(JSONErrorResponse, self).__init__(request, data)
