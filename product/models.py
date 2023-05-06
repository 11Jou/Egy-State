from django.db import models

class Buyer(models.Model):
    apertment = models.IntegerField()
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    def __str__(self) -> str:
        return str(self.apertment)