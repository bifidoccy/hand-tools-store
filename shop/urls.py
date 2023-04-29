from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    # path('shop/', views.FilterProductsView.as_view(), name='filter'),
    path('shop/', views.ProductListView.as_view(), name='product_list'),
    path('shop-filter/', views.AjaxFilterProductsView.as_view(), name='json-filter'),
    path('shop/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
]