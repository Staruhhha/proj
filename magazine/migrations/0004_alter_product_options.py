# Generated by Django 5.0 on 2023-12-15 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0003_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', '-price'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]