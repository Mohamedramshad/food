from django.db import models




# Create your models here.

class StoreCategory(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category')

    class Meta:
        db_table = 'restaurant_store_category'
        verbose_name = 'store category'
        verbose_name_plural = 'store categories'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE)
    short_discription = models.CharField(max_length=225)
    image = models.ImageField(upload_to='store')
    tagline = models.CharField(max_length=255)
    rating = models.FloatField()
    time = models.IntegerField()

    class Meta:
        db_table = 'restaurant_store'
        verbose_name = 'store'
        verbose_name_plural = 'stores'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Slider(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='slider')
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        db_table = 'restaurant_slider'
        verbose_name = 'slider'
        verbose_name_plural = 'sliders'
        ordering = ['-id']

    def __str__(self):
        return self.name
    

class Foodcategory(models.Model):
    name = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Foodcategory'
        verbose_name = 'Foodcategory'
        verbose_name_plural = 'Foodcategories'
        ordering = ['-id']

    def __str__(self):
        return self.name    
    

class Food(models.Model):
    image = models.ImageField(upload_to='slider')
    name = models.CharField(max_length=255)
    price = models.FloatField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    is_veg  = models.BooleanField(default=False)
    Foodcategory = models.ForeignKey(Foodcategory, on_delete=models.CASCADE)


    class Meta:
        db_table = 'store_food'
        verbose_name = 'food'
        verbose_name_plural = 'foods'
        ordering = ['-id']

    def __str__(self):
        return self.name        

