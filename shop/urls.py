from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('shop/', views.ProductListView.as_view(), name='product_list'),
    # path('shop/', views.list_products, name='product_list'),
    # path('shop-filter/', views.AjaxFilterProductsView.as_view(), name='json-filter'),
    path('shop/<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
]