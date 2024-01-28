from user.models import User, DateTimeAbstract
from django.db import models

class ShortenedURL(DateTimeAbstract):
    original_url = models.URLField()
    short_key = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.short_key
    
    def increase_click_count(self):
        self.click_count += 1
        self.save()

