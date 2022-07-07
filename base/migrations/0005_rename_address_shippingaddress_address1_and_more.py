# Generated by Django 4.0.5 on 2022-07-05 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_country_shippingaddress_states'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='address',
            new_name='address1',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='address2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]