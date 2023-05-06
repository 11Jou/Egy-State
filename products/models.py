from django.db import models
from django.contrib.auth.models import User

# Create your models here.
X = (
    ('Yes' , 'Yes'),
    ('No' , 'No')
)

class Apertment(models.Model):
    id = models.IntegerField(max_length=50 , default=1)
    Apertment_Id=models.IntegerField(max_length=50 , default=1 , primary_key=True)
    City = models.CharField(max_length=50)
    Location = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    Compound = models.CharField(max_length=5)
    Price = models.IntegerField()
    PriceT = models.CharField(max_length=50)
    Level = models.IntegerField()
    Area = models.IntegerField()
    Bedrooms = models.IntegerField()
    Bathrooms = models.IntegerField()
   # is_fur = models.CharField(choices=X,max_length=10)
    Delivery = models.CharField(max_length=50)
    Description = models.CharField(max_length=5000)
    Elevator = models.CharField(choices=X,max_length=10)
    Balcony = models.CharField(choices=X,max_length=10)
    Security = models.CharField(choices=X,max_length=10)
    Elc_meter = models.CharField(choices=X,max_length=10)
    Water_meter = models.CharField(choices=X,max_length=10)
    Natural_gas = models.CharField(choices=X,max_length=10)
    def _str_(self):
        return str(self.Apertment_Id)

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    City = models.CharField(max_length=50)
    Location = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    Compound = models.CharField(max_length=5)
    Bedrooms = models.IntegerField()
    Bathrooms = models.IntegerField()
    Area = models.IntegerField()
    Delivery = models.CharField(max_length=50)
    Price = models.IntegerField()

class Image(models.Model):
    Apertment_Id = models.ForeignKey(Apertment, on_delete=models.CASCADE, to_field='Apertment_Id')
    Image=models.URLField(max_length=2000)

    def _str_(self) -> str:
        return str(self.Apertment_Id)

class Connection(models.Model):
    Connection_Id=models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Apertment_Id = models.ForeignKey(Apertment, on_delete=models.CASCADE)