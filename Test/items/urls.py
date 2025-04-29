from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.items,name='items'),
    path('product_<int:item_id>/', views.items, name='item'),# URL for individual item
    
]