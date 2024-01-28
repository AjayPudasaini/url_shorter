from django.urls import path
from .views import ListURLSView, URLShortenView, RedirectOriginalURLView, DeleteShortedURLView, UpdateShortenedURLView

app_name = "short_url"

urlpatterns = [
    path("list", ListURLSView.as_view(),  name="url_lists"),
    path("create", URLShortenView.as_view(),  name="url_create"),
    path('<str:short_key>/', RedirectOriginalURLView.as_view(), name='redirect_original_url'),
    path('delete/<str:short_key>/', DeleteShortedURLView.as_view(), name='delete_shorted_url'),
    path('update/<str:short_key>/', UpdateShortenedURLView.as_view(), name='update_shorted_url'),
]
