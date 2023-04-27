from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View

from .models import Product, Category

class HomeView(View):
    
    def get(self, request):
        return render(request, 'shop/home.html', context={})

class ProductListView(ListView):
    model = Product
    paginate_by = 7

class ProductDetailView(DetailView):
    model = Product
