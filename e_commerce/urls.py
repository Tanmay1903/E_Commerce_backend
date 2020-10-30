from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django_mongoengine import mongo_admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', mongo_admin.site.urls),
    path('',include('Users.urls')),
    path('',include('Product.urls')),
    path('',include('Review.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
