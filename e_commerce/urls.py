from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django_mongoengine import mongo_admin

urlpatterns = [
    path('admin/', mongo_admin.site.urls),
    path('',include('Users.urls')),
]
