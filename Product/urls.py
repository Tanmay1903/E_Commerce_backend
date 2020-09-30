from django.conf.urls import url
from django.urls import path,include
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('addproduct/',views.Add_Products.as_view(),name='addproduct'),
    path('add_product/',TemplateView.as_view(template_name='../templates/Product/add_product.html'),name='add_product'),
    path('security/crm/',views.welcome,name='welcome'),
    path('updateproduct/<str:a>',views.UpdateProduct.as_view(),name = 'updateproduct'),
    path('update_product/<str:a>',views.update_product,name = 'update_product'),
    path('logout/',views.user_logout,name='logout'),
]
