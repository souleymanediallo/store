from django.shortcuts import render, get_object_or_404, redirect

from config import settings
from .models import Product, Order, Cart
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import stripe
stripe.api_key = settings.STRIPE_API_KEY

# Create your views here.
def home(request):
    products = Product.objects.all()[0:4]
    context = {
        'products': products
    }
    return render(request, 'products/index.html', context)


@login_required
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


@login_required
def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse('product_detail', kwargs={'slug': slug}))


@login_required
def cart(request):
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user)
    context = {
        'orders': cart.orders.all()
    }
    return render(request, 'products/cart.html', context)


@login_required
def cart_delete(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart.delete()
    return redirect('index')


def create_checkout_session(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    line_items = [{"price": order.product.stripe_id,
                   "quantity": order.quantity} for order in cart.orders.all()]
    session = stripe.checkout.Session.create(
        locale='fr',
        line_items=line_items,
        payment_method_types=['card'],
        mode='payment',
        success_url='http://127.0.0.1:8000/',
        cancel_url='http://127.0.0.1:8000/',
    )

    return redirect(session.url, code=303)
