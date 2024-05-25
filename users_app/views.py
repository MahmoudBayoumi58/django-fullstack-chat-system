from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from chat_app.models import ChatRoom
from globals.email import EmailService
from users_app.forms import UserCreationForm
from users_app.models import Users, PasswordReset, Activation
from django.utils.translation import gettext_lazy as _


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                user.is_online = True
                user.save()
                return redirect('suggested_users')
            else:
                messages.error(request, _('Activate you account'))
                return redirect('send_activation_view')
        else:
            messages.error(request, _('Invalid Credentials'))

    return render(request, 'users_app/signin.html')


@login_required
def logout_view(request):
    request.user.is_online = False
    request.user.save()
    logout(request)
    messages.success(request, _('You logged out successfully !'))
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(f'Account was created for {form.cleaned_data["email"]}'))
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'users_app/signup.html', {'form': form})


def activate_account(request, code):
    activation = Activation.objects.filter(activation_code=code).first()
    now = timezone.now()

    if not activation:
        messages.error(request, _('Invalid activation code'))
        return redirect('login')

    if (now - activation.expired_at).total_seconds() > 0:
        messages.error(request, _('Invalid / expired activation code'))
        return redirect('login')

    user = activation.user
    user.is_active = True
    user.save()

    messages.success(request, _('Account has been activated successfully'))
    return redirect('login')


def activation_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Users.objects.filter(email=email).first()
        if not user:
            messages.success(request, _('User with this email does not exist'))
            return redirect('send_activation_view')

        if user.is_active:
            messages.success(request, _('User already activated'))
            return redirect('login')

        activation = Activation(user=user)
        activation.save()
        activation_code = activation.activation_code
        activation_link = f'http://127.0.0.1:8000/user/activate/{activation_code}/'
        EmailService.send_activation_email(
            activation_link,
            from_email=settings.EMAIL_HOST_USER,
            to_emails=[user.email]
        )
        messages.success(request, _(f'Please check your mail for activation link'))
        return redirect('login')

    return render(request, 'users_app/activation_request.html')


def forget_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Users.objects.filter(email=email).first()
        if not user:
            messages.success(request, _('User with this email does not exist'))
            return redirect('login')

        if not user.is_active:
            messages.success(request, _('Activate your account'))
            return redirect('send_activation_view')

        code = PasswordReset(user=user)
        code.save()
        reset_code = code.reset_code
        reset_link = f'http://127.0.0.1:8000/user/reset-password/{reset_code}/'
        EmailService.send_reset_password_email(
            reset_link,
            from_email=settings.EMAIL_HOST_USER,
            to_emails=[user.email]
        )
        messages.success(request, _(f'Please check your mail for activation link'))
        return redirect('login')
    return render(request, 'users_app/forget-password.html')


def reset_password_view(request, code):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        password_reset = PasswordReset.objects.filter(reset_code=code).first()
        now = timezone.now()

        if not password_reset:
            messages.error(request, _('Invalid code'))
            return redirect('forget_password')

        if (now - password_reset.expired_at).total_seconds() > 0:
            messages.error(request, _('Invalid / expired code'))
            return redirect('forget_password')

        user = password_reset.user
        user.set_password(new_password)
        password_reset.expired_at = now
        user.save()
        password_reset.save()

        messages.success(request, _('Password has been changed successfully'))
        return redirect('login')

    return render(request, 'users_app/reset-password.html', {'code': code})


@login_required
def dashboard_view(request):
    return render(request, 'base/main.html')


@login_required
def settings_view(request):
    return render(request, 'users_app/settings.html')


@login_required
def suggested_users_view(request):
    # Get all chat rooms that the current user is a part of
    user_chat_rooms = ChatRoom.objects.filter(participants=request.user)

    # Get all users that the current user has not chatted with
    suggested_users = Users.objects.exclude(chat_rooms__in=user_chat_rooms).exclude(id=request.user.id)

    return render(request, 'users_app/suggested_users.html', {'suggested_users': suggested_users})


@login_required
def change_password_view(request):
    form_pass = True
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            messages.success(request, _('Password has been changed successfully !'))

        else:
            messages.error(request, _('You entered in-correct password !'))

    return render(request, 'users_app/settings.html', {'form_pass': form_pass})


@login_required
def update_user_view(request):
    form_account = True
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio').strip() if request.POST.get('bio') else None
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.bio = bio
        user.save()
        messages.success(request, _('Account info updated successfully'))

    return render(request, 'users_app/settings.html', {'form_account': form_account})
