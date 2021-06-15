from app.forms import LoginForm
from django.urls import path
from app import views, productViews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, views as auth_views
from .forms import LoginForm


urlpatterns = [
    path('', productViews.ProductView.as_view(), name = "home"),
    path('product-detail/<int:pk>', productViews.ProductDetailView.as_view(), name='product-detail'),

    path('mobile/', productViews.mobile, name='mobile'),
    path('mobile/<slug:data>', productViews.mobile, name='mobiledata'),

    path('laptop/', productViews.laptop, name='laptop'),
    path('laptop/<slug:data>', productViews.laptop, name='laptopdata'),

    path('topwear/', productViews.topwear, name='topwear'),
    path('topwear/<slug:data>', productViews.topwear, name='topweardata'),

    path('bottomwear/', productViews.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', productViews.bottomwear, name='bottomweardata'),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('checkout/', views.checkout, name='checkout'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
