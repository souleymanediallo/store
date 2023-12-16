from pprint import pprint

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from accounts.models import MyUser, ShippingAddress
from config import settings
from .models import Product, Order, Cart
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

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
        customer_email=request.user.email,
        shipping_address_collection={"allowed_countries": ["FR"]},
        success_url=request.build_absolute_uri(reverse('checkout-success')),
        cancel_url='http://127.0.0.1:8000/',
    )

    return redirect(session.url, code=303)


def checkout_success(request):
    return render(request, 'products/success.html')


@csrf_exempt
def stripe_webhook(request):
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    end_point_secret = settings.WEBHOOK_API_KEY
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key, end_point_secret, sig_header
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        data = event['data']['object']  # contains a stripe.PaymentIntent PaymentIntent was successful!
        pprint(data)
        try:
            user = get_object_or_404(MyUser, email=data['customer_email'])
        except KeyError:
            return HttpResponse("Invalid user email", status=400)

        completed_order(data=data, user=user)
        save_shipping_address(data=data, user=user)
        return HttpResponse("Adresse de livraison bien enregistrée !", status=200)

    return HttpResponse(status=200)


def completed_order(data, user):
    user.strip_id = data['customer']

    if hasattr(user, 'cart') and user.cart is not None:
        user.cart.delete()
        user.cart.save()
    return HttpResponse(status=200)


def save_shipping_address(data, user):
    try:
        shipping_info = data["shipping"]
        name = shipping_info["name"]
        address = shipping_info["address"]
        city = address["city"]
        line1 = address["line1"]
        line2 = address["line2"]
        zip_code = address["postal_code"]
    except KeyError as e:
        print("KeyError in save_shipping_address:", e)
        return HttpResponse("Invalid shipping address", status=400)

    address, created = ShippingAddress.objects.get_or_create(
        user=user,
        name=name,
        address_1=line1,
        address_2=line2 or "",
        city=city,
        zip_code=zip_code,
        country="fr"
    )
    if created:
        print("New ShippingAddress created:", address)
    else:
        print("ShippingAddress already exists:", address)

    return HttpResponse(status=200)




