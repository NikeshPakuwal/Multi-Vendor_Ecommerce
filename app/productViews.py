from django.shortcuts import render
from django.views import View
from.models import Product, Cart, OrderPlaced, Customer
from django.db.models import Q


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category = 'TW')
        bottomwears = Product.objects.filter(category = 'BW')
        mobiles = Product.objects.filter(category = 'M')
        laptops = Product.objects.filter(category = 'L')

        context = {
            'topwears' : topwears,
            'bottomwears' : bottomwears,
            'mobiles' : mobiles,
            'laptops' : laptops
        }
        return render(request, 'app/home.html', context)


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk = pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            
        context = {
            'item_already_in_cart' : item_already_in_cart,
            'product' : product
        }
        return render(request, 'app/productdetail.html', context)


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'OnePlus' or data == 'iPhone' or data == 'Samsung' or data == 'Oppo' or data == 'Gionee' or data == 'MI':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(selling_price__lt=15000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(selling_price__gt=15000)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'sony' or data == 'Apple' or data == 'Samsung' or data == 'Lenovo' or data == 'ASUS':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(selling_price__lt=50000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(selling_price__gt=50000)
    return render(request, 'app/laptop.html', {'laptops':laptops})

def topwear(request, data=None):
    if data == None:
        topWears = Product.objects.filter(category='TW')
    elif data == 'below':
        topWears = Product.objects.filter(category='TW').filter(selling_price__lt=1500)
    elif data == 'above':
        topWears = Product.objects.filter(category='TW').filter(selling_price__gt=1500)
    return render(request, 'app/topwear.html', {'topWears':topWears})

def bottomwear(request, data=None):
    if data == None:
        bottomWear = Product.objects.filter(category='BW')
    elif data == 'below':
        bottomWear = Product.objects.filter(category='BW').filter(selling_price__lt=1500)
    elif data == 'above':
        bottomWear = Product.objects.filter(category='BW').filter(selling_price__gt=1500)
    return render(request, 'app/bottomwear.html', {'bottomWear':bottomWear})