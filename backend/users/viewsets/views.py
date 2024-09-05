from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models.user import User
from users.models.address import Address
from orders.models.order import Order

from users.serializers.user_serializer import UserSerializer
from users.serializers.address_serializer import AddressSerializer
from orders.serializers.order_serializer import OrderSerializer

from django.shortcuts import get_object_or_404

class UsersSignUp(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UsersSignIn(APIView):
    def post(self, request):
        payload = request.data.copy()
        user = User.objects.get(email=payload['email'])
        if (user.password == payload['password']):
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({
            'error': {
                'message': 'E-mail ou Senha Incorreta',
                'status': '400'
            }
        }, status=status.HTTP_400_BAD_REQUEST)
        
class AddressCreate(APIView):
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
        
class GetUserAddress(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        address = user.address_set.all()
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)
        
class GetUserOrders(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        orders = user.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
        # TODO: Testar se está funcionando
        
class UsersList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
        