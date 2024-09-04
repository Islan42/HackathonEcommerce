from django.db import models

class Order(models.Model):
    shipping_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20 , choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending')
    creation_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # ordering = []
        pass
    
    def __str__(self):
        return f"{self.total}: {self.shipping_address}"