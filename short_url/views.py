import string
import random
import base64

from datetime import datetime, timedelta

from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ShortenedURL
from .utils import GenerateQR


class ListURLSView(LoginRequiredMixin, View):
    """
    View for listing URLs created by the authenticated user.

    Attributes:
        model: The model to query for shortened URLs.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve and display a list of URLs created by the authenticated user.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The rendered HTML template displaying the list of URLs.
        """
        urls = ShortenedURL.objects.filter(user=request.user)
        return render(request, "short_url/list.html", {"urls":urls})
    

class URLShortenView(LoginRequiredMixin, View):
    """
    View for shortening URLs.

    Attributes:
        model: The model representing a shortened URL.
    """

    def get(self, request):
        """
        Handle GET requests to display the URL shortening form.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered HTML template for creating a shortened URL.
        """

        return render(request, 'short_url/create.html')

    def post(self, request):
        """
        Handle POST requests to create a shortened URL.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirects to the URL list page upon successful URL creation.
            HttpResponse: The rendered HTML template for creating a shortened URL with an error message if validation fails.
        """

        original_url = request.POST.get('long_url')
        custom_url = request.POST.get('custom_url')
        expiry_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')

        if custom_url and ShortenedURL.objects.filter(custom_url_key=custom_url).exists():
            error_message = "Custom URL is already in use. Please choose a different one."
            return render(request, 'short_url/create.html', {"error_message":error_message})

        if not original_url.startswith('http://') and not original_url.startswith('https://'):
            original_url = 'http://' + original_url

        short_key = custom_url if custom_url else self.generate_short_key()

        shortened_url = ShortenedURL(original_url=original_url, short_key=short_key, user=request.user, custom_url_key=custom_url, expiration_date=expiry_date)
        shortened_url.save()

        # Generate QR code Image for the short url
        current_site = Site.objects.get_current()
        domain = current_site.domain
        scheme = request.scheme
        data = f"{scheme}://{domain}/{shortened_url.short_key}"
        obj = GenerateQR()
        qr_data = obj.generate_qr_code(data)
        qr_image_data = base64.b64decode(qr_data)

        # Save QR code
        shortened_url.qr_code.save(f"{shortened_url.short_key}.png", ContentFile(qr_image_data))

        return redirect('short_url:url_lists')

    def generate_short_key(self):
        """
        Generate a unique short key for the shortened URL.

        Returns:
            str: The generated short key.
        """

        characters = string.ascii_letters + string.digits
        short_key = ''.join(random.choice(characters) for _ in range(6))
        return short_key


class RedirectOriginalURLView(LoginRequiredMixin, View):
    """
    View for redirecting to the original URL associated with a short key.

    Attributes:
        model: The model representing a shortened URL.
    """
    def get(self, request, short_key):
        """
        Handle GET requests to redirect to the original URL.

        Args:
            request: The HTTP request object.
            short_key: The short key associated with the shortened URL.

        Returns:
            HttpResponseRedirect: Redirects to the original URL upon successful retrieval.
            HttpResponseNotFound: Returns a 404 response if the shortened URL is not found.
        """

        try:
            shortened_url = ShortenedURL.objects.get(short_key=short_key)

            if shortened_url.expiration_date and shortened_url.expiration_date < datetime.now():
                error_message = "Shorted URL has been expired."
                return redirect("short_url:url_lists")

            shortened_url.increase_click_count()

            return redirect(shortened_url.original_url)
        except ShortenedURL.DoesNotExist:
            return HttpResponseNotFound("Shortened URL not found.")     
           

class UpdateShortenedURLView(LoginRequiredMixin, View):
    """
    View for updating a shortened URL.

    Attributes:
        model: The model representing a shortened URL.
    """

    def get(self, request, short_key):
        """
        Handle GET requests to retrieve the shortened URL for updating.

        Args:
            request: The HTTP request object.
            short_key: The short key associated with the shortened URL.

        Returns:
            HttpResponse: Renders the update form with the shortened URL data.
            HttpResponseNotFound: Returns a 404 response if the shortened URL is not found.
        """

        try:
            shortened_url = ShortenedURL.objects.get(short_key=short_key)
            return render(request, "short_url/update.html", {"shortened_url": shortened_url})
        except ShortenedURL.DoesNotExist:
            return HttpResponseNotFound("Shortened URL not found.")
        
    def post(self, request, short_key):
        """
        Handle POST requests to update the shortened URL.

        Args:
            request: The HTTP request object.
            short_key: The short key associated with the shortened URL.

        Returns:
            HttpResponseRedirect: Redirects to the URL list page upon successful update.
            HttpResponseNotFound: Returns a 404 response if the shortened URL is not found.
        """

        try:
            shortened_url = ShortenedURL.objects.get(short_key=short_key)
            shortened_url.original_url = request.POST.get("long_url")
            shortened_url.save()
            return redirect("short_url:url_lists")
        except ShortenedURL.DoesNotExist:
            return HttpResponseNotFound("Shortened URL not found.")



class DeleteShortedURLView(LoginRequiredMixin, View):
    """
    View for deleting a shortened URL.

    Attributes:
        model: The model representing a shortened URL.
    """

    def get(self, request, short_key):
        """
        Handle GET requests to delete the shortened URL.

        Args:
            request: The HTTP request object.
            short_key: The short key associated with the shortened URL.

        Returns:
            HttpResponseRedirect: Redirects to the URL list page upon successful deletion.
            HttpResponseNotFound: Returns a 404 response if the shortened URL is not found.
        """

        try:
            shortened_url = ShortenedURL.objects.get(short_key=short_key)
            shortened_url.delete()
            return redirect("short_url:url_lists")
        except ShortenedURL.DoesNotExist:
            return HttpResponseNotFound("Shortened URL not found.")