from django.conf.urls import url
from django.urls import path,include
from . import views

urlpatterns = [
path('userregister/',views.UserRegister.as_view(),name='userregister'),
path('userlogin/',views.UserLogin.as_view(),name='userlogin'),
path('userlogout/',views.UserLogout.as_view(),name='userlogout'),
path('Userlist/', views.Userlist.as_view(),name='Userlist'),
]
