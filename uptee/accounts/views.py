from django.core.mail import mail_admins
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from accounts.forms import *
from settings import ADMINS, DEBUG

@login_required
def logout(request):
    user_logout(request)
    return render_to_response('accounts/logout.html', {
            'next': request.REQUEST.get('next', reverse('home')),
        }, context_instance=RequestContext(request))

def login(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if request.method == 'POST':
        post = request.POST.copy()
        next = post.get('next', '')
        form = AuthenticationForm(data=post)
        if form.is_valid():
            user_profile = User.objects.get(username=form.get_user())
        if next == reverse('logout') or next == reverse('logout')[:-1]:
            post['next'] = reverse('home')
            request.POST = post
    return auth_views.login(request, 'accounts/login.html')

@login_required
def settings(request):
    form = SettingsUserForm(instance=request.user)
    if request.method == 'POST':
        form = SettingsUserForm(request.POST,
            instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was saved successfully")
    return render_to_response('accounts/settings.html', {
            'form': form,
        }, context_instance=RequestContext(request))

@login_required
def change_password(request):
    form = PasswordChangeForm(current_user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, current_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, u'Password changed successfully.')
    return render_to_response('accounts/password_change.html', {
            'form': form,
        }, context_instance=RequestContext(request))

def register(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password1']),
                is_active=False,
            )
            new_user.save()
            messages.success(request, "Your account was successfully created. An Admin will contact you shortly.")
            if ADMINS:
                mail_admins('User registration', u'The following user just registered and wants to be activated:\r\n\r\n{0}'.format(form.cleaned_data['username']), fail_silently=not DEBUG)
            return redirect(reverse('home'))
    else:
        form = RegisterForm()
    return render_to_response('accounts/register.html', {
            'form': form,
        }, context_instance=RequestContext(request))
