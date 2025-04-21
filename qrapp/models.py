from django.db import models

# Create your models here.

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    ptr_id = models.IntegerField(null=True)
    qr_code_link = models.URLField(null=True)
    has_entered = models.BooleanField(default=False)
    got_coffee = models.BooleanField(default=False)
    email = models.CharField(max_length=100, null = True)
    is_vip = models.BooleanField(default=False)
    company = models.CharField(max_length=100, null = True)
    def __str__(self):
        return self.name