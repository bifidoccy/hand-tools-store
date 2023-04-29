from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Product, Category

class HomeView(View):
    
    def get(self, request):
        return render(request, 'shop/home.html', context={})

class ProductListView(ListView):
    model = Product
    paginate_by = 7

class ProductDetailView(DetailView):
    model = Product

# class FilterProductsView(ListView):
    
#     def get_queryset(self):
#         queryset = Product.objects.filter(
#             Q(category__in=self.request.GET.getlist('cat')) | 
#             Q(manufacturer__in=self.request.GET.getlist('mfact'))
#         )
#         return queryset


class AjaxFilterProductsView(ListView):
    
    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(category__in=self.request.GET.getlist('cat')) | 
            Q(manufacturer__in=self.request.GET.getlist('mfact')),
            photos__primary=True
        ).distinct().values('name', 'cost', 'description', 'slug', 'photos__photo')
        return queryset

    def get(self, request):
        queryset = list(self.get_queryset())
        return JsonResponse({'products': queryset}, safe=False)