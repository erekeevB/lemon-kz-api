from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Sex(models.Model):
    name = models.CharField(max_length=1, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sex"


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    sex = models.ManyToManyField(Sex)

    def __str__(self):
        return str(self.brand.name + " " + self.name)


class ItemImg(models.Model):
    img = models.URLField(max_length=200)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    isThumbnail = models.BooleanField(default=False)

    def __str__(self):
        return str(self.item.name + " / " + str(self.isThumbnail))


class Review(models.Model):
    star = models.IntegerField()
    text = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.author.username + " / " + self.item.name)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.IntegerField(choices=[(i, i) for i in range(1, 11)])

    def __str__(self):
        return str(self.user.username + " / " + self.item.name + " / " + str(self.qty))

    class Meta:
        unique_together = ("user", "item")