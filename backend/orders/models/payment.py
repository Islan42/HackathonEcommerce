from django.db import models
from orders.models.order import Order

class Payment(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('pending', 'Pending'), ('declined', 'Declined')], default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ordering = []
        pass
    
    def __str__(self):
        return f"R${self.amount}: {self.payment_status}"