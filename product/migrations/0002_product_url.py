# Generated by Django 3.1.3 on 2020-11-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.URLField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
