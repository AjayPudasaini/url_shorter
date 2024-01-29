from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """
    Form for user registration.

    This form extends the built-in UserCreationForm to include an email field.

    Attributes:
        email (forms.EmailField): Field for entering the user's email address.

    Meta:
        model (User): The User model to which the form is associated.
        fields (list): The fields to be included in the form.

    Fields:
        full_name (CharField): Field for entering the user's full name.
        email (EmailField): Field for entering the user's email address.
        password1 (CharField): Field for entering the user's password.
        password2 (CharField): Field for confirming the user's password.
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    """
    Form for user login.

    This form includes fields for entering the user's email address and password.

    Fields:
        email (EmailField): Field for entering the user's email address.
        password (CharField): Field for entering the user's password (masked for security).
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
