from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


# Create your models here.

class Food(models.Model):
    title = models.CharField(max_length=200)
    description=models.TextField()
    food_image=models.ImageField(upload_to='product')

    def __str__(self):
        return self.title


