"""
URL configuration for DivineDew project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from beautyapp import views 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from  beautyapp.forms import LoginForm, MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('pdetails/<int:pk>/', views.ProductDetail.as_view(), name='pdetails'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>/', views.updateAddress.as_view(), name='updateAddress'),
    path('add-to-cart',views.add_to_cart,name='add-to-cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/',views.show_cart,name='cart'),
    path('ulogout/', views.ulogout),
    path('checkout/', views.checkout.as_view(),name='checkout'),
    path('orders/',views.orders, name='orders'),

    path('search/',views.search,name='search'),

    # login authentication
    path('register/',views.CustomerRegistrationView.as_view(),name='register'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
   
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm, success_url='/accounts/login'), name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    #payment
    path('paymentdone/', views.payment_done, name='paymentdone'),


    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)