# Generated by Django 5.0.4 on 2024-04-15 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField()),
                ('date', models.DateField()),
                ('transaction_type', models.CharField(max_length=20)),
                ('amount', models.IntegerField()),
            ],
            options={
                'db_table': 'transactions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('annual_income', models.CharField(max_length=20)),
                ('credit_score', models.IntegerField()),
            ],
        ),
    ]
