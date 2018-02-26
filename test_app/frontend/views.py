from __future__ import unicode_literals, absolute_import
import logging
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from .forms import SignUpForm, PasswordChangeCustomForm
from django.contrib.auth.models import User
from .utils import send_templated_email

logger = logging.getLogger(__name__)


@login_required
def home(request):
    return render(request, 'frontend/index.html')


@login_required
def user_profile(request, id=None):
    logger.info("----------Request user profile ----------")
    if id:
        profile = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            profile.first_name = request.POST['first_name']
            profile.last_name = request.POST['last_name']
            profile.email = request.POST['email']
            profile.save()
            messages.add_message(request, messages.INFO, "You Profile updated successfully.")
        return render(request, 'frontend/profile.html', {'profile': profile})


def login(request):
    logger.info("----------Request for login ----------")
    template_name = "frontend/login.html"
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect("home")
        else:
            return render(request, template_name, {'error_message': 'Invalid login'})
    return render(request, template_name)


def signup(request):
    logger.info("----------Request for signup ----------")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            # base_url = request.get_host()
            # send_templated_email(subject='Company Registration Confirmation',
            #                      email_template_name='frontend/confirmation_email.html',
            #                      email_context={'user_name': form.cleaned_data.get('username'),
            #                                     'user_email': form.cleaned_data.get('email'),
            #                                     'user_password': form.cleaned_data.get('password1'),
            #                                     'base_url': base_url
            #                                     },
            #                      recipients=form.cleaned_data.get('email'))

            return HttpResponseRedirect("home")
        else:
            return render(request, 'frontend/signup.html', {'form': form, 'error_message': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'frontend/signup.html', {'form': form})


@login_required
def logout(request):
    logger.info("---------- Request for logout ----------")
    auth_logout(request)
    messages.add_message(request, messages.INFO, "You have successfully logged out.")
    return redirect("frontend:login")


@login_required
def change_password(request):
    logger.info("---------- Request for change password for user ----------")
    if request.method == 'POST':
        form = PasswordChangeCustomForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password changed successfully.")
            logger.info("Password changed successfully.")
            return redirect("frontend:change_password")
        else:
            logger.error("Failed to change password..." + str(form.errors))
            messages.error(request, 'Please correct the error below.')
            return render(request, "frontend/change_password.html", {'form': form})
    else:
        form = PasswordChangeCustomForm(user=request.user)
        args = {'form': form}
        logger.info("Trying to render user change password form.")
        return render(request, "frontend/change_password.html", args)


def page_not_found(request):
    return render(request, "frontend/404.html")


def internal_server_error(request):
    return render(request, "frontend/500.html")
