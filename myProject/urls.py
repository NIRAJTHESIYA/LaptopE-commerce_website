"""myProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from onlineShop import views
from django.conf import settings
from django.conf.urls.static import static
from onlineShop.views import *

admin.site.site_header = "HariPriya"
admin.site.index_title = "HariPriya"
admin.site.site_title = "HariPriya"

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('reg/',views.sign_up,name='reg'),
    path('login/',views.sign_in,name='login'),
    path('c_password/',views.c_password,name='c_password'),
    path('f_password/',views.f_password,name='f_password'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('productCat/<int:brand_id>/',views.productPageListView.as_view(),name='productCat'),
    path('productview/<int:pro_id>/',views.productview,name="productview"),
    # path('accesoriesCat/<int:accesories_id>/',views.accesoriesPage,name='accesoriesCat'),
    # path('accessoriesProductview/<int:acc_id>/',views.accessoriesProductview,name="accessoriesProductview"),
    path('add-to-cart', views.addtocart, name='addtocart'),
    path('cart',views.viewcart, name="cart"),
    path('allproduct',views.viewallproduct, name="allproduct"),
    path('change-quantity', views.updatecart, name="change-quantity"),
    path('delete-cart-product',views.deletecartproduct, name="delete-cart-product"),
    path('wishlist',views.viewwishlist, name='wishlist'),
    path('add-to-wishlist', views.addtoWishlist, name='add-to-wishlist'),
    path('delete-wishlist-product', views.deletewishlistproduct, name='delete-wishlist-product'),
    path('checkout', views.checkout1, name='checkout'),
    path('place-order', views.placedorder, name='place-order'),
    path('my_orders', views.myorder, name='my_orders'),
    path('view-order/<str:t_no>',views.vieworder, name='view-order'),
    path('aboutuspage', views.aboutus_page, name='aboutuspage'),
    path('findstore', views.find_store, name='findstore'),
    path('change-charges',views.changecharges,name='change-charges'),
    #  path('add-to-cart_acce', views.addtocart_accessory, name='add-to-cart_acce'),
    # path('change-quantity_accessory', views.updatecart, name="change-quantity_accessory"),
    #  path('delete-cart-accessory',views.deletecartaccessory, name="delete-cart-accessory"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
