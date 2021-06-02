from django.urls import path
from . import views

urlpatterns = [
    path('addtocart/',views.Add_to_cart.as_view(),name='addtocart'),
    path('getcart/',views.getcart.as_view(),name='getcart'),
    path('removefromcart/', views.Remove_from_cart.as_view(), name='removefromcart'),
    path('addtowishlist/',views.Add_to_Wishlist.as_view(),name='addtowishlist'),
    path('getwishlist/',views.getWishlist.as_view(),name='getwishlist'),
    path('removefromwishlist/', views.Remove_from_Wishlist.as_view(), name='removefromwishlist'),
    path('placeorder/',views.PlaceOrder.as_view(),name='placeorder'),
    path('saveforlater/',views.Save_for_Later.as_view(),name='saveforlater')
]