from django.db import models
# Create your models here.


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    pub_date = models.DateField()
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)

    def __str__(self):
        return self.user_name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    total_amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=500)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[:7] + "..."
