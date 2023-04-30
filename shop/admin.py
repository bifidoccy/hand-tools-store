from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget

from .models import *

class ProductAdminForm(forms.ModelForm):
    """ details ckeditor """
    details_ru = forms.CharField(label='Details (ru)', widget=CKEditorWidget())
    details_en = forms.CharField(label='Details (en)', widget=CKEditorWidget())
 
    class Meta:
        model = Product
        fields = '__all__'

class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 0
    max_num = 4
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width=100px height=80px>')

    get_photo.short_description = 'Фото'

class ReviewInline(admin.TabularInline):
    pass

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name',)

@admin.register(Manufacturer)
class ManufacturerAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'category', 'in_stock', 'cost', 'orders_count', 'on_sale', 'slug')
    list_display_links = ('name', )
    list_filter = ('category', 'manufacturer', 'in_stock',)
    prepopulated_fields = {'slug': ('name', )}
    actions = ('publish', 'unpublish')
    search_fields = ('name', 'category')
    readonly_fields = ('orders_count', )
    list_editable = ('on_sale',)
    save_on_top = True
    save_as = True
    inlines = [ProductPhotoInline]
    form = ProductAdminForm

    def unpublish(self, request, queryset):
        """ Снять с продажи """
        row_update = queryset.update(on_sale=False)
        message_bit = f'Обновлённых записей: {row_update}.'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """ Выставить на продажу """
        row_update = queryset.update(on_sale=True)
        message_bit = f'Обновлённых записей: {row_update}.'
        self.message_user(request, f'{message_bit}')

    unpublish.short_description = 'Снять с продажи'
    unpublish.allowed_permissions = ('change', )

    publish.short_description = 'Выставить на продажу'
    publish.allowed_permissions = ('change', )

@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ('product', 'get_photo')
    readonly_fields = ('get_photo', )
    
    def get_photo(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width=100px height=80px>')

    get_photo.short_description = 'Фото'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'product', 'ip')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'email', 'product')
    readonly_fields = ('nickname', 'email')

admin.site.register(RatingStar)