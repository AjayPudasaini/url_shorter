from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils.timezone import now


class DateTimeAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserAccountManager(BaseUserManager):
    def create_user(self, full_name, email, password=None):
        if not full_name:
            raise ValueError('User must have full name')
        
        user = self.model(
            email = self.normalize_email(email),
            full_name = full_name
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, full_name, email, password):
        user = self.create_user(
            full_name=full_name,
            email = self.normalize_email(email),
            password=password
        )

        user.is_superadmin = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True

        user.save(using=self.db)
        return user
    
class User(DateTimeAbstract, AbstractBaseUser):
    full_name = models.CharField(max_length=50)

    username = None
    email = models.EmailField(max_length=255, unique=True)
    
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    email_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserAccountManager()
    
    def __str__(self):
        return f'Account Of {self.full_name} '
    
    def has_perm(self, perm, obj=None):
        return self.is_superadmin

    def has_module_perms(self, app_label):
        return self.is_superadmin
