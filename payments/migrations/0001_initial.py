# Generated by Django 5.0.4 on 2024-04-15 22:15

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('emi_amount_principal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('emi_amount_interest', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('principal_amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.loan')),
            ],
        ),
    ]
