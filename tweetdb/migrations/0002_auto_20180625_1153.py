# Generated by Django 2.0.6 on 2018-06-25 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweetdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='created_time',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='user',
            field=models.CharField(db_index=True, max_length=15),
        ),
    ]
