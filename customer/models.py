from django.db import models
from users.models import User
from restaurant.models import Food,Store


class Customer(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        db_table = 'Customer_Customer'
        verbose_name  = 'customer'
        verbose_name_plural = 'customers'
        ordering = ['-id']


def __str__(self):
       return self.user.email  


class Cart(models.Model):
     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
     product = models.ForeignKey(Food, on_delete=models.CASCADE)
     store = models.ForeignKey(Store, on_delete=models.CASCADE)
     amount = models.FloatField()
     quantity = models.IntegerField()


     class Meta:
        db_table = 'Customer_cart'
        verbose_name  = 'cart'
        verbose_name_plural = 'carts'
        ordering = ['-id']


def __str__(self):
       return self.customer.user.email  

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=225, null=True, blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField()
    appartement = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    address_type = models.CharField(max_length=50, choices=[('home', 'Home'), ('work', 'Work'), ('other', 'Other')], default='home')    
    

    class Meta:
        db_table = 'Customer_address'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        ordering = ['-id']

    def __str__(self):
        return self.name    

class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    itemtotal = models.CharField(max_length=225)
    offerapplied = models.CharField(max_length=225)
    deliverycharges = models.CharField(max_length=225)  
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True, blank=True)  
    final_amount = models.FloatField()



    class Meta:
        db_table = 'customer_bill'
        verbose_name = 'bill'
        verbose_name_plural = 'bills'
        ordering = ['-id']

    def __str__(self):
        return self.customer.user.email   


class Offer(models.Model):
    code = models.CharField(max_length=255)
    discount = models.FloatField()
    short_description = models.CharField(max_length=255)
    is_percentage = models.BooleanField()
    
    
    class Meta:
        db_table = "customer_offer"
        verbose_name = "offer"
        verbose_name_plural = "offers"
        ordering = ["-id"]

    def _str_(self):
        return self.code