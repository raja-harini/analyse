# Generated by Django 5.1.2 on 2025-02-25 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nexus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accounttransaction',
            name='id',
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='Serial_No',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
