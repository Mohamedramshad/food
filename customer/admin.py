from django.contrib import admin

from customer.models import Customer,Cart,Address,Bill,Offer

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Bill)
admin.site.register(Offer)



