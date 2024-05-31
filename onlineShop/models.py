from django.db import models
import os

# Create your models here.

def filepath(request,filename):
    old_filename = filename
    return os.path.join('userImage/',old_filename)

def filepathProduct(request,filename):
    old_filename = filename
    return os.path.join('productImage/',old_filename)

class City(models.Model):
    idcity = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'city'
    
    def __str__(self):
        return self.city_name

class Area(models.Model):
    pincode = models.DecimalField(primary_key=True, max_digits=6, decimal_places=0)
    area_name = models.CharField(max_length=45)
    delivery_charges = models.IntegerField()
    city_idcity = models.ForeignKey(City,on_delete=models.SET_NULL,null=True,db_column='city_idcity')

    class Meta:
        managed = True
        db_table = 'area'
    
    def __str__(self):
        return self.area_name

class Store(models.Model):
    idstore = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=45)
    store_email = models.CharField(max_length=45)
    store_phone = models.DecimalField(max_digits=10, decimal_places=0)
    store_description = models.CharField(max_length=500)
    store_Address = models.CharField(max_length=500 ,null=True)
    area_pincode = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True,db_column='area_pincode')

    class Meta:
        managed = True
        db_table = 'store'
    
    def __str__(self):
        return self.store_name

class User(models.Model):
    iduser = models.AutoField(primary_key=True)
    user_fullname = models.CharField(max_length=45,null=True)
    user_name = models.CharField(max_length=45)
    user_password = models.CharField(max_length=15)
    user_email = models.CharField(max_length=45)
    user_mobile = models.CharField(max_length=10)
    user_image = models.ImageField(upload_to=filepath,null=True,blank=True)
    is_admin = models.IntegerField()
    store_idstore = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True, db_column='store_idstore')
    area_pincode = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True, db_column='area_pincode')

    class Meta:
        managed = True
        db_table = 'user'
    
    def __str__(self):
        return self.user_name
    
    def register(self):
        self.save()
        
    def isEmailexists(self):
        if User.objects.filter(user_email=self.user_email):
            return True
        return False
    
    def isphoneNumberexists(self):
        if User.objects.filter(user_mobile=self.user_mobile):
            return True
        return False
    
    def isUsernameexists(self):
        if User.objects.filter(user_name=self.user_name):
            return True
        return False

class Brand(models.Model):
    idbrand = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=45)
    brand_description = models.CharField(max_length=200)
    store_idstore = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True, db_column='store_idstore')

    class Meta:
        managed = True
        db_table = 'brand'
    
    def __str__(self):
        return self.brand_name
    
# class Accesories(models.Model):
#     idaccesories = models.AutoField(primary_key=True)
#     accesories_name = models.CharField(max_length=45)
#     accesories_description = models.CharField(max_length=200)
#     store_idstore = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True, db_column='store_idstore')

#     class Meta:
#         managed = True
#         db_table = 'accesories'
    
#     def __str__(self):
#         return self.accesories_name

class Offer(models.Model):
    idOffer = models.AutoField(primary_key=True)
    offer_start_date = models.DateField()
    offer_end_date = models.DateField()
    offer_description = models.TextField(max_length=100)
    
    def __str__(self):
        return self.offer_description

class Product(models.Model):
    idproduct = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    price = models.IntegerField()
    product_image = models.ImageField(upload_to=filepathProduct)
    product_description = models.TextField(max_length=3000)
    brand_brand_idbrand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    offer_offer_idOffer = models.ForeignKey(Offer,on_delete=models.SET_NULL,null=True)
    
    def __str__(self):
        return self.product_name
    
# class Accesories_Pro(models.Model):
#     idaccesories = models.AutoField(primary_key=True)
#     accesories_name = models.CharField(max_length=200)
#     price = models.IntegerField()
#     accesories_image = models.ImageField(upload_to=filepathProduct)
#     accesories_description = models.TextField(max_length=3000)
#     accesories_accesories_idaccesories = models.ForeignKey(Accesories,on_delete=models.SET_NULL,null=True)
#     offer_offer_idOffer = models.ForeignKey(Offer,on_delete=models.SET_NULL,null=True)
    
#     def __str__(self):
#         return self.accesories_name

class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    # accessories = models.ForeignKey(Accesories_Pro,on_delete=models.SET_NULL,null=True)
    offer_record = models.IntegerField(default=0)
    product_qty = models.IntegerField(null=True, blank=True)
    # accessories_qty = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Cart of {self.user.user_fullname}'
    
class wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    idorder = models.AutoField(primary_key=True)
    orderfullname = models.CharField(max_length=150,null=True)
    orderemail = models.CharField(max_length=150,null=True)
    ordermobile = models.CharField(max_length=150,null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_delivery_date = models.DateTimeField(auto_now_add=True)
    order_delivery_address = models.TextField(null=False)
    city = models.CharField(max_length=150,null=False)
    total_amount = models.FloatField(null=False)
    order_payment_method = models.CharField(max_length=150,null=False)
    payment_id = models.CharField(max_length=250,null=True)
    status = (
        ('Pending','Pending'),
        ('Out for shipping','Out for shipping'),
        ('Completed','Completed'),
    )
    order_status = models.CharField(max_length=150,choices=status,default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    is_cancel_order = models.IntegerField(default=0)
    area_pincode = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True)
    user_iduser = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'order'
    
    def __str__(self):
        return '{} - {}'.format(self.idorder,self.tracking_no)
    
class OrderedItem(models.Model):
    order_idorder = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    productid = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'ordered_item'
    
    # def __str__(self):
    #     return '{} - {}'.format(self.order_idorder,self.order_idorder.tracking_no)