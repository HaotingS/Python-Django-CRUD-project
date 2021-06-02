from django.db import models


# Create your models here.

class Coin(models.Model):
    name = models.CharField(max_length = 100)
    price_guess = models.DecimalField(max_digits=1000, decimal_places=8)

 



    
