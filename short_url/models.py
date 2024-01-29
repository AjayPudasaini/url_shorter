from django.db import models

from user.models import User
from utils.models import DateTimeAbstract



class ShortenedURL(DateTimeAbstract):
    """
    Model representing a shortened URL entry.

    This model stores information about a shortened URL, including the original URL,
    the generated short key, the user who created it, optional custom URL key,
    click count, associated QR code image, and expiration date.

    Attributes:
        original_url (str): The original URL that was shortened.
        short_key (str): The unique short key generated for the URL.
        user (User): The user who created the shortened URL.
        custom_url_key (str): Optional custom URL key provided by the user.
        click_count (int): The number of times the shortened URL has been clicked.
        qr_code (ImageField): The QR code image associated with the shortened URL.
        expiration_date (DateField): The expiration date of the shortened URL.

    Methods:
        __str__(): Returns a string representation of the shortened URL instance.
        increase_click_count(): Increases the click count of the shortened URL.
        get_qr_image: Returns the URL of the QR code image associated with the shortened URL.

    Inherits:
        DateTimeAbstract: Abstract model containing created_at and updated_at fields.
    """

    original_url = models.URLField()
    short_key = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_url_key = models.CharField(max_length=10, blank=True, null=True)
    click_count = models.PositiveIntegerField(default=0)
    qr_code = models.ImageField(upload_to="shorted_url/qr/", blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)


    def __str__(self):
        """
        Returns a string representation of the shortened URL instance.

        Returns:
            str: The short key of the shortened URL.
        """

        return self.short_key
    
    def increase_click_count(self):
        """
        Increases the click count of the shortened URL.
        """

        self.click_count += 1
        self.save()

    @property
    def get_qr_image(self):
        """
        Returns the URL of the QR code image associated with the shortened URL.

        Returns:
            str: The URL of the QR code image.
        """

        url = None
        if not self.qr_code:
            url = None
        else:
            url = self.qr_code.url
        return url

