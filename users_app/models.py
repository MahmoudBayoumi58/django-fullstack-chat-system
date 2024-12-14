from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from globals.email import EmailService
from .managers import CustomUserManager
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Users(AbstractUser):
    username = None
    groups = None

    email = models.EmailField(unique=True, verbose_name=_('email address'))
    picture = models.ImageField(upload_to='users_images/', default='default.png')
    phone = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    is_online = models.BooleanField(db_default=False)
    uuid = models.UUIDField(default=uuid.uuid4)
    is_active = models.BooleanField(db_default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name[:1].upper() + self.last_name[:1].upper()


def get_default_expired_at():
    return timezone.now() + timedelta(minutes=10)


class Activation(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    activation_code = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=get_default_expired_at)

    def __str__(self):
        return self.activation_code


class PasswordReset(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    reset_code = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=get_default_expired_at)

    def __str__(self):
        return self.reset_code


@receiver(post_save, sender=Users)
def send_activation_code(created, instance, **kwargs):
    if created and not instance.is_superuser:
        activation = Activation(user=instance)
        activation.save()
        activation_code = activation.activation_code
        activation_link = f'http://127.0.0.1:8000/user/activate/{activation_code}/'
        EmailService.send_activation_email(
            activation_link,
            from_email=settings.EMAIL_HOST_USER,
            to_emails=[instance.email]
        )
