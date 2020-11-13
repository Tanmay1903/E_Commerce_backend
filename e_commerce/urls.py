from django.conf.urls import url
from django.urls import path,include
from django_mongoengine import mongo_admin
from django.conf import settings
from django.conf.urls.static import static
from Users import views as user_views

urlpatterns = [
    path('admin/', mongo_admin.site.urls),
    path('',include('Users.urls')),
    path('',include('Product.urls')),
    path('',include('Review.urls')),
    path('',include('Order.urls')),
    url(r'^activate_user/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.act, name='activate_user'),
    #url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.password_reset_confirm, name='reset_password_confirm'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [url(r'^spkct/', include(urlpatterns))]