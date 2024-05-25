from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Product, Customer,Cart,Payment,OrderPlaced,Wishlist
from django.db.models import Count
from .forms import CustomerRegistrationForm,CustomerProfileForm,SearchForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import razorpay
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
def index(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'index.html',locals())
# register
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'register.html',locals())
    def post(self,request):
        form= CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"invalid data")
        return render(request,'register.html',locals())



def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'contact.html',locals())

def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'about.html',locals())

class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category= val)
        title = Product.objects.filter(category= val).values('title')
        # Logic to handle the category code
        return render(request, 'category.html', locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_wishlist = False
        item_already_in_wishlist = Wishlist.objects.filter(Q(products=product.id) & Q(user=request.user)).exists()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'products_details.html',locals())

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title= val)
        title = Product.objects.filter(category= product[0].category).values('title')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        # Logic to handle the category code
        return render(request, 'category.html', locals())
    
class ProfileView(View):
    def get(self,request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form=CustomerProfileForm()
        return render(request,"profile.html",locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data ['zipcode']
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state, zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,'Invalid Input Data' )
        return render(request,"profile.html",locals())

def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add= Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())


class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance = add);
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST);
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")
       
def ulogout(request):
    logout(request)
    return redirect("/")

def add_to_cart(request):
    
    user=request.user
    if not Customer.objects.filter(user=user).exists():
        return redirect('profile')
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user= request.user
    cart= Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount= amount+value
    totalamount = amount + 40
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'addtocart.html',locals())

def update_cart(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('increment_'):
                product_id = int(key.split('_')[1])
                cart_item = Cart.objects.filter(user=request.user, product__id=product_id).first()
                if cart_item:
                    cart_item.quantity += 1
                    cart_item.save()
                    messages.success(request, "Quantity increased successfully.")
                else:
                    messages.error(request, "Cart item not found.")
            elif key.startswith('decrement_'):
                product_id = int(key.split('_')[1])
                cart_item = Cart.objects.filter(user=request.user, product__id=product_id).first()
                if cart_item:
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                        messages.success(request, "Quantity decreased successfully.")
                    else:
                        cart_item.delete()
                        messages.success(request, "Item removed from cart.")
                else:
                    messages.error(request, "Cart item not found.")
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart_item = Cart.objects.filter(user=request.user, product__id=product_id).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Cart item not found.")
    return redirect('cart')

class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount += value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount" : razoramount,"currency": "INR","receipt":"order_rcptid_12"}
        payment_response =client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status =='created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status = order_status
            )
            payment.save() 
        return render(request, 'checkout.html', locals()) 
    

@login_required   
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')    
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart_items = Cart.objects.filter(user=user)
    for cart_item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=cart_item.product,
            quantity=cart_item.quantity,
            payment=payment
        )
        cart_item.delete()
    return redirect("orders")


def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'orders.html',locals())

from django.db.models import Q
from django.shortcuts import render

def search(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    form=SearchForm(request.GET)
    query = request.GET.get('search')
    category = form['category'].value()
    if query:
        product = Product.objects.filter(Q(title__icontains=query))
    elif category:
        product = product.filter(category=category)

    else:
        product = Product.objects.none()  # Return an empty QuerySet if no query

    context = {
        'totalitem': totalitem,
        'product': product,
        'query': query,

    }
    return render(request, 'search.html', context)

def add_to_wishlist(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    wishlist.products.add(product)
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return redirect('wishlist_view')

def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    totalitem = 0
    wishlist_length = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'wishlist.html', {'wishlist': wishlist,'totalitem' : totalitem,'wishlist_length':wishlist_length})

def remove_from_wishlist(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(user=user)
    wishlist.products.remove(product)
    return redirect('wishlist_view')