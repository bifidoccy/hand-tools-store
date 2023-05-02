from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('shop/', views.ProductListView.as_view(), name='product_list'),
    path('shop/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
]