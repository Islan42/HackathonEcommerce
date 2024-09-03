from django.db import models
from products.models.product import Product

class Order(models.Model):
    # user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20 , choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending')
    creation_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # ordering = []
        pass
    
    def __str__(self):
        return f"{self.total}: {self.shipping_address}"

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