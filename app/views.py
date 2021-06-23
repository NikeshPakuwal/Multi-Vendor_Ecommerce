from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from.models import Product, Cart, OrderPlaced, Customer
from.forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registration Sucessful!')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        context = {
            'form' : form,
            'active' : 'btn-primary'
        }
        return render(request, 'app/profile.html', context)
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()

            messages.success(request, 'Profile Updated Successfully!')

            context = {
                'form' : form,
                'active' : 'btn-primary'
            }
        return render(request, 'app/profile.html', context)

def address(request):
    add = Customer.objects.filter(user=request.user)
    context = {
        'add' : add,
        'active' : 'btn-primary'
    }
    return render(request, 'app/address.html', context)

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0.0
        shipping_amount = 50.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            context = {
                'carts' : cart,
                'amount' : amount,
                'totalamount' : totalamount
            }
            return render(request, 'app/addtocart.html', context)
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')

def orders(request):
    return render(request, 'app/orders.html')

def checkout(request):
    return render(request, 'app/checkout.html')
