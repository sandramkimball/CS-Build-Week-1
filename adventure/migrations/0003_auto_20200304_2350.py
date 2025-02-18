# Generated by Django 3.0.3 on 2020-03-04 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0002_auto_20200304_2253'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='currentRoom',
            new_name='currentChamber',
        ),
        migrations.AddField(
            model_name='chamber',
            name='d_to',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chamber',
            name='description',
            field=models.CharField(default='DEFAULT DESCRIPTION', max_length=500),
        ),
        migrations.AddField(
            model_name='chamber',
            name='e_to',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chamber',
            name='n_to',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chamber',
            name='s_to',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chamber',
            name='title',
            field=models.CharField(default='DEFAULT TITLE', max_length=50),
        ),
        migrations.AddField(
            model_name='chamber',
            name='u_to',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chamber',
            name='w_to',
            field=models.IntegerField(default=0),
        ),
    ]
