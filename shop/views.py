from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Product, Category

class HomeView(View):
    """ Main page """
    def get(self, request):
        return render(request, 'shop/home.html', context={})

class ProductListView(ListView):
    """ Products List """
    model = Product
    paginate_by = 4

    def get_queryset(self):
        """ Getting params """
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
        
        """ Create paginator object as p """
        self.p = self.get_paginator(queryset, self.paginate_by)
        return queryset
    
    def get_context_data(self):
        sort = self.request.GET.get('sort', 'none')
        view = self.request.GET.get('view', 'list')
        page_number = self.request.GET.get('page', 1)
        page_object = self.p.get_page(page_number)

        """ num1 and num2 are variables in '.list-inline nav' in product_list.html """
        num1 = 1
        num2 = len(page_object.object_list)
        for i in range(int(page_number)-1):
            if page_object.has_next() == False:
                num1 += self.paginate_by
            else:
                num1 += len(page_object.object_list)
            if num2 + len(page_object.object_list) <= self.p.count:
                num2 += self.paginate_by

        context = super().get_context_data()

        """ Sending params in template """
        context['mfact'] = ''.join([f'mfact={x}&' for x in self.request.GET.getlist('mfact')])
        context['cat'] = ''.join([f'cat={x}&' for x in self.request.GET.getlist('cat')])
        context['sort'] = f'sort={sort}&'
        context['view'] = f'view={view}&'
        context['num1'] = num1
        context['num2'] = num2
        return context

class ProductDetailView(DetailView):
    """ Product """
    model = Product

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
