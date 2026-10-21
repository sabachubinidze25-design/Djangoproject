from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop_list, name="shop_list"),
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    path("sale/", views.sale_products, name="sale_products"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("product/add/", views.product_create, name="product_create"),
    path("product/<int:product_id>/edit/", views.product_update, name="product_update"),
    path("product/<int:product_id>/delete/", views.product_delete, name="product_delete"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("contact/", views.contact, name="contact"),
]
