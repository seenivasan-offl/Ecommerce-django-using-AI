"""
URL configuration for ecom_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from ecom_app.views import edit_profile, login_view, order_confirmation, order_history, register_view, user_logout, product_list, product_detail, home_view, cart_view, profile_view, admin_dashboard, staff_dashboard, add_to_cart, remove_from_cart, checkout_view,search_product,ajax_search,add_to_wishlist, remove_from_wishlist, wishlist_view,move_to_cart
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', product_list, name='home'),
    path('', home_view, name='home'),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path('logout/', user_logout, name='logout'),
    path('products/', product_list, name='products'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('cart/', cart_view, name='cart'),  # Define the 'cart' URL
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('profile/', profile_view, name='profile'),  # Define the 'profile' URL
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    # path('remove-from-cart/<int:product_id>/',
    #      remove_from_cart, name='remove_from_cart'),
    # path('remove-from-cart/<int:product_id>/',
    #      remove_from_cart, name='remove-from-cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('order-confirmation/', order_confirmation, name='order_confirmation'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('orders/', order_history, name='order_history'),
    path('search/', search_product, name='search_product'),
    path('ajax_search/', ajax_search, name='ajax_search'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', wishlist_view, name='wishlist_view'),
    path('wishlist/move-to-cart/<int:product_id>/', move_to_cart, name='move_to_cart'),
]

if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
