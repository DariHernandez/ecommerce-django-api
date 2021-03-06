from django.db import models

# Create your models here.
class User (models.Model):
    name = models.CharField (max_length=100)
    api_key = models.CharField (max_length=32)
    to_email = models.CharField (max_length=250)

class FromEmail (models.Model):
    email = models.CharField (max_length=50)
    password = models.CharField (max_length=16)

class History (models.Model):
    datetime = models.DateTimeField (auto_now_add=True)
    user = models.ForeignKey (User, on_delete=models.SET_NULL, null=True)
    subject = models.CharField (max_length=250, default=None)

    def __str__ (self):
        return f"{self.datetime} {self.user.name} {self.subject}"

class BlackList (models.Model):
    to_email = models.CharField (max_length=250)

    def __str__ (self):
        return self.to_email
