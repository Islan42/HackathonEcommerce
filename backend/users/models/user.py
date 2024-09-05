from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}: {self.email}"