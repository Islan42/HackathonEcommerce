from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from orders.models.order import Order
from orders.models.order_item import OrderItem
from orders.models.payment import Payment
from products.models.product import Product
from orders.serializers.order_serializer import OrderSerializer

class OrdersList(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrdersCreate(APIView):
    def post(self, request):
        payload = request.data.copy()
        
        order = Order.objects.create(
            shipping_address=payload['shipping_address'],
            total=0
        )
        order.save()

        for product in payload['products']:
            productObject = get_object_or_404(Product, pk=product['product_id'])
            orderItemPrice = productObject.price * product['quantity']

            order_item = OrderItem.objects.create(
                order_id=order,
                product_id=productObject,
                quantity=product['quantity'],
                price=orderItemPrice
            )
            order_item.save()

            order.total += orderItemPrice
        
        order.save()
        
        payment = Payment.objects.create(
            order_id=order,
            payment_method=payload['payment_method'],
            amount=order.total
        )
        payment.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)

class OrdersDelete(APIView):
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)