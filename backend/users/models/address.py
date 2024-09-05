from django.db import models
from users.models.user import User

class Address(models.Model):
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.postal_code}"