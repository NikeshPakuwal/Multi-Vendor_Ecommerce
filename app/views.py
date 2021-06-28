from django.http import request
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from.models import Product, Cart, OrderPlaced, Customer
from.forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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

@method_decorator(login_required, name='dispatch')
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

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
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

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=request.user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount

    return render(request, 'app/checkout.html', {'add' : add, 'totalamount' : totalamount, 'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed' : op})


def buy_now(request):
    return render(request, 'app/buynow.html')