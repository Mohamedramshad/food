from django.contrib import admin

# Register your models here.
 

from restaurant.models import StoreCategory, Store, Slider,Food,Foodcategory

admin.site.register(StoreCategory)
admin.site.register(Store)
admin.site.register(Slider)
admin.site.register(Food)
admin.site.register(Foodcategory)








