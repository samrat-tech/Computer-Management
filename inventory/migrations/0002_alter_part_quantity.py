# Generated by Django 3.2.7 on 2022-05-02 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]