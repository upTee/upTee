from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.defaults import page_not_found, permission_denied, server_error
from accounts.models import get_template


def home(request):
    return render_to_response('{0}/base.html'.format(get_template(request)), context_instance=RequestContext(request))


def about(request):
    return render_to_response('{0}/about.html'.format(get_template(request)), context_instance=RequestContext(request))


def custom_page_not_found(request):
    return page_not_found(request, template_name='{0}/404.html'.format(get_template(request)))


def custom_permission_denied(request):
    return permission_denied(request, template_name='{0}/403.html'.format(get_template(request)))


def custom_server_error(request):
    return server_error(request, template_name='{0}/500.html'.format(get_template(request)))
