from django.urls import path
from web import views

app_name = "web"


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("add-address/", views.add_address, name="add_address"),
    path("restaurants/<int:id>/", views.restaurants, name="restaurants"),
    path("singlerestaurant/<int:id>/", views.singlerestaurant, name="singlerestaurant"),
    path("add/<int:id>/", views.add_cart, name="add_cart"),
    path("plus/<int:id>/", views.plus_cart, name="plus_cart"),
    path("mines/<int:id>/", views.mines_cart, name="mines_cart"),
    path("cart/", views.cart, name="cart"),
    path("address/", views.address, name="address"),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete-item'),
    path('set_address/<int:item_id>/', views.set_address, name='set_address'),
    path('checkout', views.checkout, name='checkout'),









 

]