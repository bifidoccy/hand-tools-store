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

class FilterProductsView(ListView):

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(category__in=self.request.GET.getlist('cat')) | 
            Q(manufacturer__in=self.request.GET.getlist('mfact'))
        )
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['mfact'] = self.request.GET.getlist('mfact')
        context['cat'] = self.request.GET.getlist('cat')
        return context

class SortListView(ListView):
    
    def get_queryset(self):
        sort = self.request.GET.get('sort')
        cat = self.request.GET.getlist('cat')
        mfact = self.request.GET.getlist('mfact')
        if cat != [] or mfact != []:
            queryset = Product.objects.filter(
                Q(category__in=cat) | 
                Q(manufacturer__in=mfact),
            )
        else:
            queryset = Product.objects.all()

        if sort == 'cheap':
            queryset = queryset.order_by('cost')
        elif sort == 'expen':
            queryset = queryset.order_by('-cost')
        
        return queryset
        
    def get_context_data(self):
        context = super().get_context_data()
        context['sort'] = self.request.GET.get('sort')
        return context

# class AjaxFilterProductsView(ListView):

#     def get_params(self):
#         queryset = None
#         category = self.request.GET.getlist('cat')
#         manufacturer = self.request.GET.getlist('mfact')
#         sort = self.request.GET.getlist('sort')
#         ajax_queryset = Product.objects.filter(
#             Q(category__in=self.request.GET.getlist('cat')) | 
#             Q(manufacturer__in=self.request.GET.getlist('mfact')),
#             photos__primary=True,
#         ).distinct().values('name', 'cost', 'description', 'slug', 'photos__photo')

#         if sort == 'expen':
#             queryset = ajax_queryset.order_by('cost')
#         elif sort == 'cheap':
#             queryset = ajax_queryset.order_by('-cost')

#         return queryset
    
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
