from django.urls import path
from . import views

urlpatterns = [
path('userrating/',views.User_Review.as_view(),name='userrating'),
path('updatereview/',views.Update_Review.as_view(),name='updatereviw'),
path('deletereview/',views.delete_Review.as_view(),name='deletereview'),
path('getreview/',views.Get_Review.as_view(),name='getreview'),

]
