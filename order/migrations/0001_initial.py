# Generated by Django 4.2 on 2023-04-09 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='clientOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_name', models.CharField(max_length=150, verbose_name='OrderName')),
                ('description', models.TextField(verbose_name='Description')),
                ('order_price', models.PositiveIntegerField(verbose_name='Price')),
                ('image', models.ImageField(blank=True, null=True, upload_to='order_image/')),
                ('deadline', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='orderProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderStatus', models.IntegerField(blank=True, choices=[(1, 'Pending'), (2, 'Onprogress'), (3, 'Completed')], null=True)),
            ],
        ),
    ]
