from django.db import models
from django.contrib.auth.models import User
from .tshirt_properties import Brand, Color, Occasion, IdealFor,NeckType,Sleeve


class Tshirt(models.Model):
    name=models.CharField(max_length=50,null=False)
    slug=models.CharField(max_length=200,null=False,unique=True,default="")
    description=models.CharField(max_length=500,null=False)
    discount=models.IntegerField(default=0)
    image=models.ImageField(upload_to = 'upload/images/',null=False)
    occasion=models.ForeignKey(Occasion,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    sleeve=models.ForeignKey(Sleeve,on_delete=models.CASCADE)
    neck_type=models.ForeignKey(NeckType,on_delete=models.CASCADE)
    ideal_for=models.ForeignKey(IdealFor,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)

    def __str__(self):
        #return self.ideal_for.__str__()+"--"+self.name
        return self.name
