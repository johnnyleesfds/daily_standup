# Generated by Django 3.0.5 on 2020-04-28 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
        ('standups', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='standup',
            unique_together={('person', 'date')},
        ),
    ]
