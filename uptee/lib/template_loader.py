import os
from django.template.loaders.filesystem import Loader as FileSystemLoader
from accounts.models import get_template
import settings


class Loader(FileSystemLoader):

    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template = settings.DEFAULT_TEMPLATE
            request = getattr(settings, 'request_handler', None)
            template_dirs = settings.TEMPLATE_DIRS
            if request:
                template = get_template(request)
            template_dirs = [os.path.join(path, template) for path in template_dirs]
            template_dirs = tuple(template_dirs)
        return super(Loader, self).get_template_sources(template_name, template_dirs)
