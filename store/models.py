from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )  # This '+' tells django not to make a reverse relationship

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        ordering = ["title"]


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(
        null=True, blank=True
    )  # null: to make it accept null in database level, blank: make it accept null in admin interface
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)]
    )
    inventory = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
    )
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name="products")
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["title"]


class Customer(models.Model):
    class MembershipChoices(models.TextChoices):
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
        choices=MembershipChoices.choices,
        default=MembershipChoices.BRONZE,
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["first_name", "last_name"]


class Order(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "P", "Pending"
        COMPLETE = "C", "Complete"
        FAILED = "F", "Failed"

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="orders")


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.IntegerField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.PROTECT)
    # can not delete prodect when it is insid an ordre
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="orderitems")
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.pk)


class CartItem(models.Model):
    cart = models.ForeignKey(
        "Cart", on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self) -> str:
        return str(self.product)

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
