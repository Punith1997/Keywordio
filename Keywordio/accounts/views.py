from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages, auth
from .utils import send_verification_email

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.decorators import login_required

# Create your views here.

def register_view(request):
    error_dict = {}
    value_dict = {}
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('crud_home')
    elif request.method == 'POST':
        post = True
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.save()
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Check your email for verification!")
            return redirect('register_view')
        else:
            # print("non valid form")
            for field in form:
                value_dict[field.name] = request.POST.get(field.name)
                if field.errors:
                    for error in field.errors:
                        error_dict[field.name] = error
            # print(error_dict)
            # print(value_dict)
            # return redirect('register_view')
            pass
    else:
        form = UserForm()
        post = False
        # print(form.errors)
    context = {
        'form': form,
        'error_dict': error_dict,
        'value_dict': value_dict,
        'post': post,
    }
    return render(request, 'accounts/register.html', context)

def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations Your account is activated")
        return redirect('login_view')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('login_view')

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('crud_home')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('crud_home')
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect('login_view')
    return render(request, 'accounts/login.html')

@login_required(login_url='login_view')
def logout_view(request):
    auth.logout(request)
    messages.info(request, "You are logged out.")
    return redirect('login_view')

def forgot_password_view(request):
    # print("pressed")
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact = email)
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Password reset link has been sent to your email address")
            return redirect('login_view')
        else:
            messages.error(request, "Account does not exist")
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, "This link has been expired!")
        return redirect('login_view')

def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session['uid']
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('login_view')
        else:
            messages.error(request, 'Password do not match')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')
