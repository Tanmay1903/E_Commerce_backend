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
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('searchproduct/',views.Search_product.as_view(),name = 'searchproduct'),
    path('search_product/',views.search,name='search_product'),
    path('delete_product/<str:a>',views.delete_product,name='delete_product'),
    path('delete_fpic/',views.DeleteFrontPic.as_view(),name='delete_fpic'),
    path('delete_bpic/',views.DeleteBackPic.as_view(),name='delete_bpic'),
    path('product_list/',views.product_list.as_view(),name='product_list'),
    path('get_product/<str:a>',views.get_product.as_view(),name='get_product'),
]
