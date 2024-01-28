from django.shortcuts import render
from django.views import View


class UserLogin(View):
    def get(self, request, *args, **kwargs):
        return render(request, "user/login.html")