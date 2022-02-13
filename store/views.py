import json
from sqlite3 import complete_statement
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
 

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.CartItmTtl
    else: 
        items = []
        order = {'CartTtl': 0, 'CartItmTtl': 0, 'shipping': False}
        cartItems = order['CartItmTtl']

    products = Product.objects.all()
    context = {'products': products, 'items' :items, 'order' :order, 'cartItems' : cartItems}
    
    
    return render(
        request, 'store/store.html', context
    )


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'CartTtl': 0, 'CartItmTtl': 0, 'shipping': False}
    context = {'items': items, 'order': order}
    return render(
        request, 'store/cart.html', context
    )


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'CartTtl': 0, 'CartItmTtl': 0, 'shipping': False}
    context = {'items' :items, 'order' :order}

    return render(
        request, 'store/checkout.html', context
    )


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: , action')
    print('productId:', productId )

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1

    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added to cart', safe=False)

