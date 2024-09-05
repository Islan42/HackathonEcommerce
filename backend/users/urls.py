from django.urls import path
from users.viewsets import views

urlpatterns = [
    path('users/signup/', views.UsersSignUp.as_view()),
    path('users/signin/', views.UsersSignIn.as_view()),
    path('user/address/', views.AddressCreate.as_view()),
    path('user/<int:user_id>/address/', views.GetUserAddress.as_view()),
    path('user/<int:user_id>/orders/', views.GetUserOrders.as_view()),
    path('users/', views.UsersList.as_view()),
]