from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Product, Category

class HomeView(View):
    
    def get(self, request):
        return render(request, 'shop/home.html', context={})

class ProductListView(ListView):
    model = Product
    paginate_by = 4

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'none')
        cat = self.request.GET.getlist('cat')
        mfact = self.request.GET.getlist('mfact')
        queryset = Product.objects.all()

        if mfact != [] or cat != []:
            queryset = Product.objects.filter(
                Q(category__in=cat) | 
                Q(manufacturer__in=mfact)
            ).distinct()
        
        if sort == 'expen':
            queryset = queryset.order_by('-cost')
        elif sort == 'cheap':
            queryset = queryset.order_by('cost')
        self.p = self.get_paginator(queryset, self.paginate_by)
        return queryset
    
    def get_context_data(self):
        sort = self.request.GET.get('sort', 'none')
        page_number = self.request.GET.get('page', 1)
        page_object = self.p.get_page(page_number)
        paginate = self.paginate_by

        num1 = 1
        num2 = len(page_object.object_list)
        for i in range(int(page_number)-1):
            if page_object.has_next() == False:
                num1 += paginate
            else:
                num1 += len(page_object.object_list)
            if num2 + len(page_object.object_list) <= self.p.count:
                num2 += paginate

        context = super().get_context_data()
        context['mfact'] = ''.join([f'mfact={x}&' for x in self.request.GET.getlist('mfact')])
        context['cat'] = ''.join([f'cat={x}&' for x in self.request.GET.getlist('cat')])
        context['sort'] = f'sort={sort}&'
        context['num1'] = num1
        context['num2'] = num2
        return context

class ProductDetailView(DetailView):
    model = Product

def list_products(request):
    product_list = Product.objects.all()

    p = Paginator(product_list, 2)
    page = request.GET.get('page')
    products = p.get_page(page)

    return render(request, 'shop/product_list.html', context={'product_list': products})

# class AjaxFilterProductsView(ListView):
    
#     def get_queryset(self):
#         queryset = Product.objects.filter(
#             Q(category__in=self.request.GET.getlist('cat')) | 
#             Q(manufacturer__in=self.request.GET.getlist('mfact')),
#             photos__primary=True,
#         ).distinct().values('name', 'cost', 'description', 'slug', 'photos__photo')
#         return queryset

#     def get(self, request):
#         queryset = list(self.get_queryset())
#         return JsonResponse({'products': queryset}, safe=False)
