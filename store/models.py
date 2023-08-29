from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.models.DateTimeField(auto_now=True)


class Customer(models.Model):
    class MEMBERSHIP_CHOICES(models.TextChoices):
        BRONZE = 'B','Bronze'
        SILVER = 'C','Silver'
        GOLD = 'F','Gold'
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique= True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null = True)
    membership = models.models.CharField(max_length=1,choices =MEMBERSHIP_CHOICES.choices,default = MEMBERSHIP_CHOICES.BRONZE )


class Order(models.Model):
    class PAYMENT_STATUS(models.TextChoices):
        PENDING = 'P','Pending'
        COMPLETE = 'C','Complete'
        FAILED = 'F','Failed'

    placed_at = models.DateTimeField(auto_now_add= True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS.choices,default=PAYMENT_STATUS.PENDING)