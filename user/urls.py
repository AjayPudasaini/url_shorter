from django.urls import path
# from url_shorter.user.views import UserLogin
from .views import UserLoginView, UserRegister
from django.contrib.auth import views as auth_views

app_name = "user"

urlpatterns = [
    path("", UserLoginView.as_view(), name="user_login"),
    path("register", UserRegister.as_view(), name="user_register"),
    path('logout/', auth_views.LogoutView.as_view(), name='user_logout'),
]
