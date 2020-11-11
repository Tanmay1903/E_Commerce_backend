from django.urls import path
from . import views

urlpatterns = [
    path('addtocart/',views.Add_to_cart.as_view(),name='addtocart'),
    path('getcart/',views.getcart.as_view(),name='getcart'),
    path('removefromcart/', views.Remove_from_cart.as_view(), name='removefromcart'),
]