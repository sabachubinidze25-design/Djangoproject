from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import ProductForm
from .models import Product, Category


def home(request):
    products = Product.objects.select_related(
        "category").filter(available=True).order_by("price")
    categories = Category.objects.annotate(
        product_count=Count("products")).order_by("name")
    return render(request, "shop/home.html", {"products": products, "categories": categories})


def shop_list(request):
    products = Product.objects.select_related(
        "category"
    ).all().order_by("price")

    categories = Category.objects.annotate(
        product_count=Count("products")
    ).order_by("name")

    category_id = request.GET.get("category", "")

    if category_id:
        products = products.filter(category_id=category_id)

    return render(
        request,
        "shop/shop.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": category_id,
        },
    )


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.select_related(
        "category").filter(category=category).order_by("price")
    return render(request, "shop/category.html", {"category": category, "products": products})


def sale_products(request):
    products = Product.objects.select_related(
        "category").filter(is_on_sale=True).order_by("price")
    return render(request, "shop/sale.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related("category"), id=product_id)
    return render(request, "shop/product_detail.html", {"product": product})


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, f'Product "{product.name}" was added successfully.')
            return redirect("product_detail", product_id=product.pk)
    else:
        form = ProductForm()
    return render(request, "shop/product_form.html", {"form": form, "page_title": "Add product", "button_text": "Add product"})


def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(
                request, f'Product "{product.name}" was updated successfully.')
            return redirect("product_detail", product_id=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "shop/product_form.html", {"form": form, "product": product, "page_title": "Edit product", "button_text": "Save changes"})


def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" was deleted.')
        return redirect("shop_list")
    return render(request, "shop/product_confirm_delete.html", {"product": product})


def contact(request):
    return render(request, "shop/contact.html")


def cart(request):
    return render(request, "shop/cart.html")


def checkout(request):
    return render(request, "shop/checkout.html")
