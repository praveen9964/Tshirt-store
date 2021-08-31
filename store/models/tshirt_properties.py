from django.db import models
from django.contrib.auth.models import User


class TshirtProperty(models.Model):
    title=models.CharField(max_length=30,null=False)
    slug=models.CharField(max_length=30,null=False,unique=True)   #slug is for admin reference ,admin can add any name any attribute to display in url
                                                                #unique is True bcoz slug cannot be same to others also
    def __str__(self):       #this for showing names insted of showing brand object(6) in admin site
        return self.title      #now the names will be displayed instead of object(6) or object(7) like that
# Create your models here.
class Occasion(TshirtProperty):
    pass
   

class IdealFor(TshirtProperty):
    pass    

class NeckType(TshirtProperty):
    pass
   
class Sleeve(TshirtProperty):
    pass
    

class Brand(TshirtProperty):
    pass
   

class Color(TshirtProperty):
    pass   

