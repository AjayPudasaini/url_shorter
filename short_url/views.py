import string
import random

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ShortenedURL

from django.http import HttpResponseNotFound


class ListURLSView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        urls = ShortenedURL.objects.filter(user=request.user)
        return render(request, "short_url/list.html", {"urls":urls})
    


class URLShortenView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'short_url/create.html')

    def post(self, request):
        original_url = request.POST.get('long_url')
        if not original_url.startswith('http://') and not original_url.startswith('https://'):
            original_url = 'http://' + original_url

        short_key = self.generate_short_key()

        shortened_url = ShortenedURL(original_url=original_url, short_key=short_key, user=request.user)
        shortened_url.save()

        return redirect('short_url:url_lists')

    def generate_short_key(self):
        characters = string.ascii_letters + string.digits
        short_key = ''.join(random.choice(characters) for _ in range(6))
        return short_key


class RedirectOriginalURLView(View):
    def get(self, request, short_key):
        try:
            shortened_url = ShortenedURL.objects.get(short_key=short_key)
            shortened_url.increase_click_count()
            return redirect(shortened_url.original_url)
        except ShortenedURL.DoesNotExist:
            return HttpResponseNotFound("Shortened URL not found.")     
           

class UpdateShortenedURLView(View):
    def get(self, request, short_key):
        try:
            shortened_url = ShortenedURL.objects.get(short_key=short_key)
            return render(request, "short_url/update.html", {"shortened_url": shortened_url})
        except ShortenedURL.DoesNotExist:
            return HttpResponseNotFound("Shortened URL not found.")
        
    def post(self, request, short_key):
        try:
            shortened_url = ShortenedURL.objects.get(short_key=short_key)
            shortened_url.original_url = request.POST.get("long_url")
            shortened_url.save()
            return redirect("short_url:url_lists")
        except ShortenedURL.DoesNotExist:
            return HttpResponseNotFound("Shortened URL not found.")



class DeleteShortedURLView(View):
    def get(self, request, short_key):
        try:
            shortened_url = ShortenedURL.objects.get(short_key=short_key)
            shortened_url.delete()
            return redirect("short_url:url_lists")
        except ShortenedURL.DoesNotExist:
            return HttpResponseNotFound("Shortened URL not found.")