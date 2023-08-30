from django.db import models


class Promotion(models.Model):
     description = models.CharField(max_length=255)
     discount = models.FloatField()
class Collection(models.Model):
     title = models.CharField(max_length=255)
     featured_product = models.ForeignKey('Product',on_delete=models.SET_NULL,null = True,related_name='+')
    # This '+' tells django not to make a reverse relationship
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
class Customer(models.Model):
    class MEMBERSHIP_CHOICES(models.TextChoices):
        BRONZE = "B", "Bronze"
        SILVER = "C", "Silver"
        GOLD = "F", "Gold"

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1,
        choices=MEMBERSHIP_CHOICES.choices,
        default=MEMBERSHIP_CHOICES.BRONZE,
    )

class Order(models.Model):
    class PAYMENT_STATUS(models.TextChoices):
        PENDING = "P", "Pending"
        COMPLETE = "C", "Complete"
        FAILED = "F", "Failed"

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS.choices, default=PAYMENT_STATUS.PENDING
    )
    customer = models.ForeignKey("Customer", on_delete=models.PROTECT)

class Address(models.Model):
        street = models.CharField(max_length=255)
        city = models.CharField(max_length=255)
        # Customer = models.OneToOneField(Customer, on_delete=models.CASCADE,primary_key= True)
        customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

class OrderItem(models.Model):
     order = models.ForeignKey("Order", on_delete=models.PROTECT)
     product = models.ForeignKey("Product",on_delete=models.PROTECT)
     quantity = models.PositiveSmallIntegerField()
     unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
     created_at = models.DateTimeField(auto_now = True)

class CartItem(models.Model):
     cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
     product = models.ForeignKey("Product",on_delete=models.CASCADE)
     quantity = models.PositiveSmallIntegerField()