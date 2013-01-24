import settings


class TemplateMiddleware(object):

    def process_request(self, request):
        settings.request_handler = request
