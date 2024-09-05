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
        try:
            payload = request.data.copy()
            
            order = Order.objects.create(
                shipping_address=payload['shipping_address'],
                total=0
            )
            order.save()

            order_item_list = []
            targeted_products_list = []
            
            for product in payload['products']:
                productObject = get_object_or_404(Product, pk=product['product_id'])
                orderItemPrice = productObject.price * product['quantity']

                if (productObject.stock_quantity - product['quantity'] >= 0):
                    productObject.stock_quantity -= product['quantity']
                    # productObject.save()
                    targeted_products_list.append(productObject)
                else:
                    raise ProductStockOutError

                order_item = OrderItem.objects.create(
                    order_id=order,
                    product_id=productObject,
                    quantity=product['quantity'],
                    price=orderItemPrice
                )
                order_item.save()
                order_item_list.append(order_item)

                order.total += orderItemPrice
            
            order.save()
            
            payment = Payment.objects.create(
                order_id=order,
                payment_method=payload['payment_method'],
                amount=order.total
            )
            payment.save()

            for target in targeted_products_list:
                target.save()

            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except (Exception, ProductStockOutError) as exc:
            if ('order' in locals()):
                order.delete()
            if ('order_item_list' in locals()):
                for order_item in order_item_list:
                    order_item.delete()
            if ('payment' in locals()):
                payment.delete()
            return Response(
                {
                    'error': {
                        'message': 'Erro: Bad Request', #Usar exc.msg?
                        'status': 400
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class OrdersDelete(APIView):
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductStockOutError(Exception):
    pass