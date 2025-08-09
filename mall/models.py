from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator #import for ratings



class Category(models.Model):
        name = models.CharField(max_length=100)
        slug = models.SlugField(max_length=100, unique=True)
        description = models.TextField(blank=True)
        
        class Meta:
            verbose_name_plural = 'Categories'  # we define for plural representation

        def __str__(self):
            return self.name
        

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) # One category under e multiple products and related_name why we use one category multiple products.
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) #100.11
    stock = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
        
    def __str__(self):
        return self.name
        
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.count() > 0:
            return sum([rating.rating for rating in ratings]) / ratings.count()
        return 0
    

class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE) # One product can have multiple ratings when we use ratings_name we can get all product ratings
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)   
        
    class Meta:
        unique_together = ('product', 'user')  # user respect one particular product rating unique

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}"  
    


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
        
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())   #when a customer adds items to the cart we get price total

    def get_total_item(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} X {self.product.name}"

    def get_cost(self):
        return self.product.price * self.quantity              