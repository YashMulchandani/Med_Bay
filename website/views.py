from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse

import datetime
from .models import *

def index(request):
    return render(request, 'index.html', {})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def contact(request):
    if request.method == "POST":
        c_fname = request.POST['c_fname']
        c_lname = request.POST['c_lname']
        c_email = request.POST['c_email']
        c_message = request.POST['c_message']

        # Send an E-mail
        send_mail(
            c_fname,# Subject
            c_message,# Message
            c_email,# from_email
            ['yash.mulchandani575@gmail.com'],# to_email
            )

        return render(request, 'contact.html', {'c_fname':c_fname})
    else:
        return render(request, 'contact.html', {})

def about(request):
    return render(request, 'about.html', {})


def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products':products})


def shop_single(request, id):
    data = Product.objects.get(id=id)
    return render(request, 'shop_single.html', {'data':data})


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0 ,'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']

    return render(request, 'cart.html', {'items':items, 'order':order})

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0 ,'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']

    return render(request, 'checkout.html', {'items':items, 'order':order})


def updateItem(request):
    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId', productId)

    customer = request.user.customer
    product = product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

    if orderItem.quantity <=0:
       orderItem.delete()

    return UserResponse('item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['from']['total'])
        order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
        order.save()

    if order.shipping == True:
        shippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],

        )
    else:
        print('user is not logged in..')
        return Response('payment-complete!', safe=False)
