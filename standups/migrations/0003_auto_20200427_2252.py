# Generated by Django 3.0.5 on 2020-04-28 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standups', '0002_auto_20200427_2215'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='accomplishment',
            unique_together={('standup', 'description')},
        ),
        migrations.AlterUniqueTogether(
            name='blocker',
            unique_together={('standup', 'description')},
        ),
        migrations.AlterUniqueTogether(
            name='workingon',
            unique_together={('standup', 'description')},
        ),
    ]
