from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from utils.models import DateTimeAbstract

class UserAccountManager(BaseUserManager):
    """
    Custom user manager for the User model.

    This manager provides methods to create regular users and superusers.

    Methods:
        create_user(full_name, email, password=None): Creates and saves a regular user with the given full name, email, and password.
        create_superuser(full_name, email, password): Creates and saves a superuser with the given full name, email, and password.

    Attributes:
        None
    """

    def create_user(self, full_name, email, password=None):
        """
        Create and save a regular user with the given full name, email, and password.

        Args:
            full_name (str): The full name of the user.
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            User: The created user instance.
        """

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
        """
        Create and save a superuser with the given full name, email, and password.

        Args:
            full_name (str): The full name of the superuser.
            email (str): The email address of the superuser.
            password (str): The password of the superuser.

        Returns:
            User: The created superuser instance.
        """

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
    """
    Custom user model representing a user account.

    This model extends the AbstractBaseUser class to provide custom user functionality.

    Attributes:
        full_name (str): The full name of the user.
        email (str): The email address of the user (unique).
        is_superadmin (bool): Indicates if the user is a super admin.
        is_admin (bool): Indicates if the user is an admin.
        is_staff (bool): Indicates if the user is staff.
        is_active (bool): Indicates if the user account is active.
        email_verified (bool): Indicates if the user's email is verified.
        date_joined (datetime): The date and time when the user account was created.
        last_login (datetime): The date and time when the user last logged in.
        USERNAME_FIELD (str): The field used as the unique identifier for the user (email).
        REQUIRED_FIELDS (list): The required fields when creating a user (full_name).

    Methods:
        __str__(): Returns a string representation of the user instance.
        has_perm(perm, obj=None): Determines if the user has the specified permission.
        has_module_perms(app_label): Determines if the user has permissions to access the specified app module.

    Managers:
        objects (UserAccountManager): The custom manager for the User model.
    """

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
        """
        Returns a string representation of the user instance.

        Returns:
            str: The string representation of the user instance (full name).
        """

        return f'Account Of {self.full_name} '
    
    def has_perm(self, perm, obj=None):
        """
        Determines if the user has the specified permission.

        Args:
            perm (str): The permission to check.
            obj (object): The object to check permissions for (default=None).

        Returns:
            bool: True if the user has the permission, False otherwise.
        """

        return self.is_superadmin

    def has_module_perms(self, app_label):
        """
        Determines if the user has permissions to access the specified app module.

        Args:
            app_label (str): The label of the app module.

        Returns:
            bool: True if the user has permissions, False otherwise.
        """

        return self.is_superadmin
