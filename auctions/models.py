from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField


class User(AbstractUser):
    pass

objects=models.Manager()
class auction(models.Model):
    Book = 'Book'
    Electronics = 'Electronics'
    Toys = 'Toys'
    Shoes = 'Shoes'
    other = 'other'
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    title=models.CharField(max_length=64)
    describe = models.CharField(max_length=300)
    bid = models.IntegerField(default=0)
    image = models.URLField(blank=True, null=True)
    choice = ((Book, 'BOOK'),
                    (Electronics, 'Electronics'),
                    (Toys, 'Toys'),
                    (Shoes, 'Shoes'),
                    (other, 'other',))

    category = models.CharField(max_length=60,
                              choices=choice,
                              default=Book)

    def __str__(self):
        return str(self.user)

class bid(models.Model):
    user=models.CharField(max_length=64)
    title=models.CharField(max_length=64)
    bid=models.IntegerField()

class comment(models.Model):
    user = models.CharField(max_length=64)
    commentsa = models.CharField(max_length=140,blank=True,null=True)
    listid = models.IntegerField(default=0)

class watchs(models.Model):
    user = models.CharField(max_length=64)
    auctionh = models.IntegerField()

class Closebid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listid = models.IntegerField()
    bidprice = models.IntegerField()
    image1 = models.URLField(blank=True, null=True)

