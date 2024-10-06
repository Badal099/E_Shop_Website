from django.urls import path
from Store import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('product/', views.Products.as_view(), name='product'),
    path('cart/', views.CartItems.as_view(), name='cart'),
    path('signup/', views.CustomerSignUp.as_view(), name='signup'),
    path('login/', views.CustomerLogin.as_view(), name='login'),
    path('logout/', views.CustomerLogout.as_view(), name='logout'),
    path('details/<int:pk>/', views.ProductDetails.as_view(), name='details'),
    path('check-out/', views.CheckOut.as_view(), name='checkout'),
    path('orders/', views.Orders.as_view(), name='orders'),
]

