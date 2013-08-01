from __future__ import unicode_literals

from django.core.exceptions import MiddlewareNotUsed
from django.utils.encoding import DjangoUnicodeDecodeError

from pipeline.conf import settings
from pipeline.html_utils import minify_html_leave_whitespace

if settings.PIPELINE_MINIFY_HTML_LEAVE_WHITESPACE:
    minify_html = minify_html_leave_whitespace
else:
    from django.utils.html import strip_spaces_between_tags as minify_html


class MinifyHTMLMiddleware(object):
    def __init__(self):
        if settings.DEBUG:
            # On debug does not minify html
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        if request.path.startswith('/admin/'):
            return response

        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
            try:
                response.content = minify_html(response.content.strip())
            except DjangoUnicodeDecodeError:
                pass
        return response
