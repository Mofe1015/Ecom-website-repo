import json
from sqlite3 import complete_statement
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
 

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

def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.transaction_id = transaction_id
        if float(total) == float(order.CartTtl):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                state=data['shipping']['state'],
                city=data['shipping']['city'],
                zipcode=data['shipping']['zip']
                

            )





    else:
        print('unregistered user')
    return JsonResponse('PAYMENT COMPLETE', safe=False)
