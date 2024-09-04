from django.db import models
from orders.models.order import Order
from products.models.product import Product

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # ordering = []
        pass
    
    def __str__(self):
        return f"{self.order_id}, {self.product_id} - {self.quantity} - R${self.price}"