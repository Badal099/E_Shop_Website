from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from Store.models import Product, Categories, Carousal, Customer, Order
from django.views import View
from Store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator

# Create your views here.
class HomePage(View):
    def get(self, request):
        carousal = Carousal.objects.all()
        context = {
            'carousal': carousal,
        }
        return render(request, 'home.html', context)

class Products(View):
    def get(self, request):
        products = None
        categories = Categories.objects.all()
        categoryId = request.GET.get('category')
        if categoryId:
            products = Product.objects.filter(category=categoryId)
        else:
            products = Product.objects.all()
        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, 'product.html', context)
    
    def post(self, request):
        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity - 1
                else:
                    cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart = {}
            cart[product_id] = 1

        request.session['cart'] = cart
        return redirect('product')

class CartItems(View):
    def get(self, request):
        products = []
        if request.session.get('cart'):
            cart = request.session.get('cart').keys()
            products = Product.objects.filter(id__in=cart)
        context = {
            'products': products
        }
        return render(request, 'cart.html', context)

class ProductDetails(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        context = {
            'product': product
        }
        return render(request, 'details.html', context)

class CustomerSignUp(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if not Customer.objects.filter(email=email).exists():
            if len(name) < 2:
                messages.error(request, 'Name length should be more then 2')
                return redirect('signup')
            elif len(phone) < 10:
                messages.error(request, 'Please Enter Correct Phone Number')
                return redirect('signup')
            elif len(password) < 6:
                messages.error(request, 'Password length should be more then 5')
                return redirect('signup')
            else:
                password = make_password(password)
                customer = Customer(name=name, email=email, phone=phone,password=password)
                customer.save()
                return redirect('login')
        else:
            messages.info(request, 'Email already available.')
            return redirect('signup')

class CustomerLogin(View):
    return_url = None
    def get(self, request):
        CustomerLogin.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        try:
            customer = Customer.objects.get(email=email)
            customer_password = check_password(password, customer.password)
            if customer_password:
                request.session['customer'] = customer.id
                if CustomerLogin.return_url:
                    return HttpResponseRedirect(CustomerLogin.return_url)
                else:
                    CustomerLogin.return_url = None
                    return redirect('home')
            else:
                messages.info(request, 'Password is incorrect.')
                return redirect('login')
        except:
            messages.info(request, 'Invalid Credential!!!')
            return redirect('login')

class CustomerLogout(View):
    def get(self, request):
        request.session.clear()
        logout(request)
        return redirect('login')

class CheckOut(View):
    @method_decorator(auth_middleware)
    def post(self, request):
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        customer = request.session.get("customer")
        cart = request.session.get('cart')
        products = Product.objects.filter(id__in=list(cart.keys()))
        
        for product in products:
            order = Order(address = address,
                          phone = phone,
                          customer = Customer(id=customer),
                          product = product,
                          price = product.price,
                          quantity = cart.get(str(product.id))
                          )
            order.save()
            
        request.session['cart'] = {}
        return redirect('cart')

class Orders(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        customer_id = request.session.get('customer')
        orders = Order.objects.filter(customer = customer_id)
        context = {
            'orders': orders
        }
        return render(request, 'orders.html', context)
