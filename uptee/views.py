from django.shortcuts import render_to_response
from django.template import RequestContext
from accounts.models import get_template


def home(request):
    return render_to_response('{0}/base.html'.format(get_template(request)), context_instance=RequestContext(request))


def about(request):
    return render_to_response('{0}/about.html'.format(get_template(request)), context_instance=RequestContext(request))
