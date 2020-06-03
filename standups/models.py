from django.db import models
from team.models import Person
from goals.models import Goal
import pandas as pd
from collections import namedtuple

# Create your models here.
class Standup(models.Model):
    date = models.DateField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('person', 'date',)

    def __str__(self):
        return str(self.person) + "-" + str(self.date)

    @property
    def week(self):
        return self.date.isocalendar()[1]

    def create_tuple(self, d):
        Deliverable = namedtuple("Deliverable", 'Week Person Category ProductFeature Goal Description ExpectedVelocity UnexpectedVelocity TotalVelocity')
        goal = d.goal.name if d.goal else ""
        product_feature = str(d.product_feature) if d.product_feature else ""
        return Deliverable(d.week, str(d.person), d.category, product_feature, goal,
                           d.description, d.expected, d.unexpected, d.total)

    def to_dataframe(self):
        deliverables = []
        for d in self.accomplishment_set.all():
            deliverables.append(self.create_tuple(d))

        for d in self.workingon_set.all():
            deliverables.append(self.create_tuple(d))

        for d in self.blocker_set.all():
            deliverables.append(self.create_tuple(d))

        return pd.DataFrame(deliverables)


class Deliverable(models.Model):
    standup = models.ForeignKey(Standup, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.description

    class Meta:
        abstract = True
        unique_together = ('standup', 'description',)

    @property
    def person(self):
        return self.standup.person

    @property
    def date(self):
        return self.standup.date

    @property
    def week(self):
        return self.standup.week

    @property
    def product_feature(self):
        return self.goal.tracker.product_feature if self.goal else None

    @property
    def expected(self):
        return 1 if self.goal is not None else 0

    @property
    def unexpected(self):
        return 1 if self.goal is None else 0

    @property
    def total(self):
        return self.expected + self.unexpected


class Accomplishment(Deliverable):
    @property
    def category_order(self):
        return 0

    @property
    def category(self):
        return "What did I accomplished on yesterday?"


class WorkingOn(Deliverable):
    @property
    def category_order(self):
        return 1

    @property
    def category(self):
        return "What will I work on today?"


class Blocker(Deliverable):
    @property
    def category_order(self):
        return 2

    @property
    def category(self):
        return "Are there any blockers or risks?"
