from django.db import models
from django.contrib.auth.models import User
from store.models.tshirt import Tshirt   


class SizeVariant(models.Model):
    SIZES=(
        ("S","Small"),                    # S is for Database and Small is to show in admin site
        ("M","Medium"),
        ("L","Large"),
        ("XL","Extra Large"),
        ("XXL","Extra Extra Large")
    )
    price=models.IntegerField(null=False)      #price should not be NULL so false
    tshirt=models.ForeignKey(Tshirt,on_delete=models.CASCADE)
    size=models.CharField(choices=SIZES,max_length=5)   #choices will be shown as drop down list

    def __str__(self):
        return f'{self.size}'