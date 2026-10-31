from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.core.paginator import Paginator

from .forms import ProductForm
from .models import Product, Category


class HomeView(TemplateView):
    template_name = "shop/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.select_related(
            "category"
        ).filter(available=True).order_by("price")

        paginator = Paginator(products, 8)
        page_number = self.request.GET.get("page")

        context["products"] = paginator.get_page(page_number)

        context["categories"] = Category.objects.annotate(
            product_count=Count("products")
        ).order_by("name")

        return context


class ShopListView(ListView):
    model = Product
    template_name = "shop/shop.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        products = Product.objects.select_related(
            "category"
        ).all().order_by("price")

        category_id = self.request.GET.get("category", "")

        if category_id:
            products = products.filter(category_id=category_id)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.annotate(
            product_count=Count("products")
        ).order_by("name")

        context["selected_category"] = self.request.GET.get("category", "")

        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "shop/category.html"
    context_object_name = "category"
    pk_url_kwarg = "category_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.select_related(
            "category"
        ).filter(category=self.object).order_by("price")

        paginator = Paginator(products, 8)
        page_number = self.request.GET.get("page")

        context["products"] = paginator.get_page(page_number)

        return context


class SaleProductsView(ListView):
    model = Product
    template_name = "shop/sale.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        return Product.objects.select_related(
            "category"
        ).filter(is_on_sale=True).order_by("price")


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    def get_queryset(self):
        return Product.objects.select_related("category")


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/product_form.html"
    login_url = "login"

    def get_success_url(self):
        return reverse_lazy(
            "product_detail",
            kwargs={"product_id": self.object.pk}
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == "POST":
            kwargs["files"] = self.request.FILES

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add product"
        context["button_text"] = "Add product"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        response = super().form_valid(form)

        messages.success(
            self.request,
            f'Product "{self.object.name}" was added successfully.'
        )

        return response


@login_required(login_url="login")
def product_update(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        user=request.user
    )

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():
            product = form.save()

            messages.success(
                request,
                f'Product "{product.name}" was updated successfully.'
            )

            return redirect("product_detail", product_id=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "shop/product_form.html",
        {
            "form": form,
            "product": product,
            "page_title": "Edit product",
            "button_text": "Save changes",
        },
    )


@login_required(login_url="login")
def product_delete(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        user=request.user
    )

    if request.method == "POST":
        name = product.name
        product.delete()

        messages.success(request, f'Product "{name}" was deleted.')

        return redirect("shop_list")

    return render(
        request,
        "shop/product_confirm_delete.html",
        {"product": product},
    )


class ContactView(TemplateView):
    template_name = "shop/contact.html"


class CartView(TemplateView):
    template_name = "shop/cart.html"


class CheckoutView(TemplateView):
    template_name = "shop/checkout.html"
