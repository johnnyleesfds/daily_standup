import numpy as np
import pandas as pd
from trackers.models import *
from goals.models import *
from team.models import *
from standups.models import *
import datetime
from collections import namedtuple
from IPython.display import display, HTML, Markdown
import matplotlib.pyplot as plt


def printmd(string):
    display(Markdown(string))


def clean_string(s):
    return s.replace(u'\xa0', u' ').strip()


def import_trackers(file_path):
    trackers = pd.read_csv(file_path)
    for i, r in trackers.iterrows():
        query = Tracker.objects.filter(product_feature=r["Product Feature"])
        if not query:
            Tracker(product_feature=r["Product Feature"]).save()


def import_goals(file_path):
    d = datetime.datetime.now()
    while d.weekday() != 0:
        if d.weekday() > 5:
            d += datetime.timedelta(days=1)
        else:
            d -= datetime.timedelta(days=1)

    goals = pd.read_csv(file_path, header=None)
    t, g = None, None

    for i, r in goals.iterrows():
        r = r[0]
        r = clean_string(r)
        query = Tracker.objects.filter(product_feature=r)
        if query:
            t, g = query[0], None
        else:
            g = r
        if t and g:
            query = Goal.objects.filter(tracker=t, name=g, date=d.date())
            if not query:
                Goal(tracker=t, name=g, date=d.date()).save()


def import_team(file_path):
    team = pd.read_csv(file_path)

    for i, r in team.iterrows():
        query = Person.objects.filter(**r)
        if not query:
            Person(**r).save()


def find_person(words):
    if len(words) > 1:
        query = Person.objects.filter(first_name=words[0], last_name=words[1])
        if query:
            return query[0]


def find_standup(person, date):
    query = Standup.objects.filter(person=person, date=date)
    if query:
        return query[0]
    else:
        standup = Standup(person=person, date=date)
        standup.save()
    return standup


def find_deliverable(standup, s):
    if standup:
        if "yesterday" in s.lower() or 'friday' in s.lower():
            return standup.accomplishment_set
        elif 'today' in s.lower():
            return standup.workingon_set
        elif 'blocker' in s.lower():
            return standup.blocker_set


def import_standups(file_path):
    standups = pd.read_csv("standup.csv")
    deliverable = None
    standups['Date'] = pd.to_datetime(standups['Date']).dt.date
    standups["Text"] = standups["Text"].apply(clean_string)

    for i, r in standups.iterrows():
        text = r['Text']
        date = r['Date']
        words = text.split(" ")
        person = find_person(words) if find_person(words) else person
        standup = find_standup(person, date) if find_standup(person, date) else standup
        deliverable = find_deliverable(standup, text) if find_deliverable(standup, text) else deliverable
        if not find_deliverable(standup, text) and not find_person(words):
            try:
                deliverable.create(description=text)
            except:
                pass


def standups_by_week(week=None):
    standups = Standup.objects.filter(date__week=week) if week else Standup.objects.all()
    deliverables = pd.concat([s.to_dataframe() for s in standups])

    return deliverables