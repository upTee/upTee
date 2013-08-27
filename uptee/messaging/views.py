from django.contrib import messages
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from messaging.forms import ContactForm
from settings import ADMINS, DEBUG


def contact(request):
    admins_available = True if ADMINS else False
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = u'From: {0}\r\n\r\nMessage: {1}'.format(form.cleaned_data['email'], form.cleaned_data['message'])
            mail_admins('User contact', msg, fail_silently=not DEBUG)
            messages.success(request, 'Your message has been sent.')
            return HttpResponseRedirect(reverse('home'))
    return render_to_response('messaging/contact.html', {
            'form': form,
            'admins_available': admins_available,
        }, context_instance=RequestContext(request))
