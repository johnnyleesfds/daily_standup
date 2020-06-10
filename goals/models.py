from django.db import models
from trackers.models import Tracker
from django.utils import timezone


# Create your models here.
class Goal(models.Model):
    date = models.DateField()
    tracker = models.ForeignKey(Tracker, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ('name', 'date',)

        indexes = [
            models.Index(fields=['name', 'date']),
            models.Index(fields=['name']),
            models.Index(fields=['date']),
        ]

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now()
        return super(Goal, self).save(*args, **kwargs)

    @property
    def week(self):
        return self.date.isocalendar()[1]

    def __str__(self):
        # return self.name
        return "Week" + " " + str(self.week) + ": " + self.tracker.product_feature + ":  " + self.name
