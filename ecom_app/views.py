from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.http import JsonResponse
from .models import Product, UserInteraction
from .recommendation import recommend_products, recommend_products_based_on_user

from django.shortcuts import render

def edit_profile(request):
    return render(request, 'profile/edit_profile.html')

def order_confirmation(request):
    return render(request, 'ecom_app/order_confirmation.html')
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order
from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')  # Show only logged-in user's orders
    return render(request, 'ecom_app/order_history.html', {'orders': orders})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()
        return redirect("profile")  # Redirect to profile page after saving

    return render(request, "ecom_app/edit_profile.html")
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order

def checkout_view(request):
    cart = request.session.get('cart', {})  # Retrieve session-based cart
    cart_items = []
    total_price = 0

    if not cart:  # Check if cart is empty before proceeding
        return render(request, "ecom_app/checkout.html", {"cart_items": [], "error": "Your cart is empty!"})

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({
            "name": product.name,
            "price": product.price,
            "quantity": quantity,
            "image": product.image.url
        })
        total_price += product.price * quantity

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        # Save each cart item as an Order
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                product=product,
                quantity=quantity,
                name=name,
                email=email,
                address=address,
                payment_method=payment_method
            )

        # Clear cart after order is placed
        request.session["cart"] = {}

        return redirect("order_confirmation")  

    return render(request, "ecom_app/checkout.html", {"cart_items": cart_items, "total_price": total_price})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "ecom_app/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use.")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                user.save()
                messages.success(request, "Registration successful! Please login.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'ecom_app/register.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def home_view(request):
    recommended_products = []
    if request.user.is_authenticated:
        recommended_products = recommend_products_based_on_user(request.user.id)
    if not recommended_products:
        recommended_products = Product.objects.all().order_by('?')[:5]
    products = Product.objects.all()
    return render(request, 'ecom_app/home.html', {
        'recommended_products': recommended_products,
        'products': products,
    })


def product_list(request):
    products = Product.objects.all()
    return render(request, "ecom_app/product_list.html", {"products": products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    recommended_products = recommend_products(product.id)

    if request.user.is_authenticated:
        UserInteraction.objects.update_or_create(
            user=request.user,
            product=product,
            interaction_type='view',
            defaults={'timestamp': timezone.now()}
        )

    return render(request, 'ecom_app/product_detail.html', {
        'product': product,
        'recommended_products': recommended_products,
    })


def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({'success': True, 'cart_item_count': sum(cart.values())})
    return JsonResponse({'success': False})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({'name': product.name, 'price': product.price, 'quantity': quantity, 'image': product.image.url})
        total_price += product.price * quantity
    return render(request, 'ecom_app/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def profile_view(request):
    return render(request, 'ecom_app/profile.html')


def is_staff(user):
    return user.is_staff


def admin_dashboard(request):
    users_data = []
    users = User.objects.all()
    for user in users:
        recommended_products = recommend_products(user.id)
        recommendations = [{'product': product, 'reason': "Recommended based on user behavior"} for product in recommended_products]
        users_data.append({'user': user, 'recommendations': recommendations})
    return render(request, 'ecom_app/admin_dashboard.html', {'users_data': users_data})


@user_passes_test(is_staff)
def staff_dashboard(request):
    users_data = []
    users = User.objects.all()
    for user in users:
        recommended_products = recommend_products(user.id)
        recommendations = [{'product': product, 'reason': "Recommended based on user behavior"} for product in recommended_products]
        users_data.append({'user': user, 'recommendations': recommendations})
    return render(request, 'ecom_app/staff_dashboard.html', {'users_data': users_data})


from django.shortcuts import render
from django.http import JsonResponse
from .models import Product

def search_product(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    
    return render(request, '', {'products': products, 'query': query})

def ajax_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)[:5] if query else []
    
    results = [{'id': p.id, 'name': p.name} for p in products]
    return JsonResponse(results, safe=False)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product

def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist = request.session.get('wishlist', {})
        wishlist[str(product_id)] = wishlist.get(str(product_id), 0) + 1
        request.session['wishlist'] = wishlist
        request.session.modified = True
        return JsonResponse({'success': True, 'wishlist_item_count': sum(wishlist.values())})
    return JsonResponse({'success': False})

from django.shortcuts import redirect

def move_to_cart(request, product_id):
    """Move an item from the wishlist to the cart"""
    wishlist = request.session.get('wishlist', {})
    cart = request.session.get('cart', {})

    if str(product_id) in wishlist:
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        del wishlist[str(product_id)]
        request.session['cart'] = cart
        request.session['wishlist'] = wishlist
        request.session.modified = True

    return redirect('cart')  # ✅ Fix: Ensure this matches the URL name in urls.py



def remove_from_wishlist(request, product_id):
    """Remove an item from the wishlist"""
    wishlist = request.session.get('wishlist', {})
    wishlist.pop(str(product_id), None)
    request.session['wishlist'] = wishlist
    request.session.modified = True
    return redirect('wishlist_view')  # Ensure 'wishlist_view' exists in `urls.py`
    wishlist = request.session.get('wishlist', {})
    wishlist.pop(str(product_id), None)
    request.session['wishlist'] = wishlist
    request.session.modified = True
    return redirect('wishlist_view')

def wishlist_view(request):
    wishlist = request.session.get('wishlist', {})
    wishlist_items = []
    total_price = 0
    for product_id, quantity in wishlist.items():
        product = get_object_or_404(Product, id=product_id)
        wishlist_items.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
            'image': product.image.url
        })
        total_price += product.price * quantity
    return render(request, 'ecom_app/wishlist.html', {'wishlist_items': wishlist_items, 'total_price': total_price})
