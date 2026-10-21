from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("shop/", views.ShopListView.as_view(), name="shop_list"),
    path(
        "category/<int:category_id>/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("sale/", views.SaleProductsView.as_view(), name="sale_products"),
    path(
        "product/<int:product_id>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "product/add/",
        views.ProductCreateView.as_view(),
        name="product_create",
    ),
    path(
        "product/<int:product_id>/edit/",
        views.product_update,
        name="product_update",
    ),
    path(
        "product/<int:product_id>/delete/",
        views.product_delete,
        name="product_delete",
    ),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("contact/", views.ContactView.as_view(), name="contact"),
]

