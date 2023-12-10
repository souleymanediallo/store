from django.shortcuts import render, get_object_or_404
from .models import Product


# Create your views here.
def home(request):
    products = Product.objects.all()[0:4]
    context = {
        'products': products
    }
    return render(request, 'products/index.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    return render(request, 'products/product-detail.html', context)


def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/product-list.html', context)