from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, LoginForm
from django.contrib.auth import authenticate, login


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
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
    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            return redirect("user:user_login")
        else:
            return render(request, "user/register.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        context = {"form": form}
        return render(request, "user/register.html", context)