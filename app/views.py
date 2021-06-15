from django.http import request
from django.shortcuts import render
from django.views import View
from.models import Product, Cart, OrderPlaced, Customer
from.forms import CustomerRegistrationForm
from django.contrib import messages


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


def add_to_cart(request):
     return render(request, 'app/addtocart.html')

def buy_now(request):
    return render(request, 'app/buynow.html')

def profile(request):
    return render(request, 'app/profile.html')

def address(request):
    return render(request, 'app/address.html')

def orders(request):
    return render(request, 'app/orders.html')

def change_password(request):
    return render(request, 'app/changepassword.html')

def checkout(request):
    return render(request, 'app/checkout.html')
