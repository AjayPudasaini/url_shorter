from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login

from .forms import UserRegisterForm, LoginForm


class UserLoginView(View):
    """
    View for user login functionality.

    This view handles both GET and POST requests for user login. 
    On GET request, it renders the login form.
    On POST request, it validates the form data, authenticates the user, 
    and logs in the user if the provided credentials are valid.

    Methods:
        get(self, request): Handles GET requests for user login.
        post(self, request): Handles POST requests for user login.

    Template:
        'user/login.html': The template containing the login form.

    Form:
        LoginForm: The form used to collect user login information.
    """

    def get(self, request):
        """
        Handles GET requests for user login.

        Renders the login form.

        Args:
            request (HttpRequest): The HTTP GET request.

        Returns:
            HttpResponse: Rendered response containing the login form.
        """

        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        """
        Handles POST requests for user login.

        Validates the form data, authenticates the user, and logs in the user 
        if the provided credentials are valid. Otherwise, renders the login form 
        with an error message.

        Args:
            request (HttpRequest): The HTTP POST request.

        Returns:
            HttpResponse: Rendered response containing the login form.
        """

        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('short_url:url_lists')
            else:
                error_message = "Invalid email or password."
                return render(request, 'user/login.html', {'form': form, 'error_message': error_message})
        else:
            return render(request, 'user/login.html', {'form': form})


class UserRegister(View):
    """
    View for user registration functionality.

    This view handles both GET and POST requests for user registration. 
    On GET request, it renders the registration form.
    On POST request, it validates the form data, saves the user if the provided
    information is valid, and redirects to the login page upon successful registration.

    Methods:
        get(self, request, *args, **kwargs): Handles GET requests for user registration.
        post(self, request, *args, **kwargs): Handles POST requests for user registration.

    Template:
        'user/register.html': The template containing the registration form.

    Form:
        UserRegisterForm: The form used to collect user registration information.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for user registration.

        Validates the form data, saves the user if the provided information is valid,
        and redirects to the login page upon successful registration. Otherwise, renders
        the registration form with validation errors.

        Args:
            request (HttpRequest): The HTTP POST request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirects to the login page upon successful registration, 
            or renders the registration form with validation errors.
        """

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            return redirect("user:user_login")
        else:
            return render(request, "user/register.html", {"form": form})

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for user registration.

        Renders the registration form.

        Args:
            request (HttpRequest): The HTTP GET request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Rendered response containing the registration form.
        """

        form = UserRegisterForm()
        context = {"form": form}
        return render(request, "user/register.html", context)