# -*- coding: utf-8 -*-

try:
    import cStringIO as StringIO
except:
    import StringIO

import cgi

from xhtml2pdf import pisa

from django import http
from django.template.loader import render_to_string
from django.conf import settings


def render_to_pdf(request, template_name, dictionary=None, encoding='utf-8'):
    html = render_to_string(template_name, dictionary)
    result = StringIO.StringIO()
    pdf = pisa.CreatePDF(StringIO.StringIO(html.encode(encoding)), result)
    if not pdf.err:
        response = http.HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = "filename=fichero.pdf"
        response['Pragma'] = "no-cache"
        response['Expires'] = "0"
        return response
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))


def print_debug(message, *args, **kwargs):
    if settings.DEBUG:
        print message
        if args:
            print "args", args
        if kwargs:
            print "kwargs", kwargs
