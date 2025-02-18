# Generated by Django 3.0.3 on 2020-03-05 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0003_auto_20200304_2350'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Mars',
        ),
        migrations.AlterField(
            model_name='chamber',
            name='d_to',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='chamber',
            name='e_to',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='chamber',
            name='n_to',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='chamber',
            name='s_to',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='chamber',
            name='u_to',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='chamber',
            name='w_to',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
