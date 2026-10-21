from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Product, Category


def home(request):
    products = Product.objects.filter(
        available=True
    ).order_by('price')

    categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
    })


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).order_by('price')

    return render(request, 'shop/category.html', {
        'category': category,
        'products': products,
    })


def sale_products(request):
    products = Product.objects.filter(is_on_sale=True).order_by('price')

    return render(request, 'shop/sale.html', {
        'products': products,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'shop/product_detail.html', {
        'product': product,
    })
