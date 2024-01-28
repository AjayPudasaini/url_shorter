from django.urls import path
# from url_shorter.user.views import UserLogin
from .views import UserLogin

app_name = "user"

urlpatterns = [
    path("", UserLogin.as_view(), name="user_login")
]
