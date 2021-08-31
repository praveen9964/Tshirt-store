from django.db import models
from django.contrib.auth.models import User
from .tshirt import Tshirt 
from .size import SizeVariant

class Cart(models.Model):
    #tshirt required but its already in sizeVariant
    sizeVariant=models.ForeignKey(SizeVariant,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
