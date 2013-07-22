from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from testingstate.forms import MoreKeysForm


@login_required
def generate_testing_keys(request):
    if not request.user.is_staff:
        raise Http404
    new_keys = None
    form = MoreKeysForm()
    if request.method == 'POST':
        form = MoreKeysForm(request.POST)
        if form.is_valid():
            form.save()
            new_keys = form.new_keys
            messages.success(request, "Created {0} new key{1}!".format(len(new_keys), '' if len(new_keys) == 1 else 's'))
    return render_to_response('testingstate/generate_testing_keys.html', {
            'new_keys': new_keys,
            'form': form,
        }, context_instance=RequestContext(request))
