from django.db import models

# Create your models here.
class Tracker(models.Model):
    product_feature = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.product_feature

