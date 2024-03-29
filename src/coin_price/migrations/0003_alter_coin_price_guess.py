# Generated by Django 3.2.3 on 2021-05-31 13:14

import coin_price.models
from django.db import migrations, models
from django.core.exceptions import ValidationError

def validate_zero(self, *args, **kwargs):
    if self.cleaned_data.get("price_guess") <= 0:
        raise ValidationError(
            'Price cannot be negative or zero!'
        )
class Migration(migrations.Migration):

    dependencies = [
        ('coin_price', '0002_alter_coin_price_guess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='price_guess',
            field=models.DecimalField(decimal_places=8, max_digits=1000, validators=[validate_zero]),
        ),
    ]
