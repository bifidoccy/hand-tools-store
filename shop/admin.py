from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(ProductPhoto)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Review)