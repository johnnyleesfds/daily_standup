from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        unique_together = ("first_name", "last_name")