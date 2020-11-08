from django.conf.urls import url
from django.urls import path,include
from . import views

urlpatterns = [
    path('userregister/',views.UserRegister.as_view(),name='userregister'),
    path('userlogin/',views.UserLogin.as_view(),name='userlogin'),
    path('userlogout/',views.UserLogout.as_view(),name='userlogout'),
    path('Userlist/', views.Userlist.as_view(),name='Userlist'),
    path('resendver/',views.ResendVerificationAPI.as_view(),name='resendver'),
    path('emailupdate/',views.EmailupdateAPI.as_view(),name = 'emailupdate'),
    path('passwordchange/',views.PasswordResetView.as_view(),name='passwordchange'),
    path('firstnameupdate/',views.update_firstname.as_view(),name='firstnameupdate'),
    path('lastnameupdate/',views.update_lastname.as_view(),name='lastnameupdate'),
    url(r'^forgot_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.Passwordupdateview.as_view(), name='forgot_password'),

]
