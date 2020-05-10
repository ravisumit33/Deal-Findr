# Generated by Django 3.0.6 on 2020-05-10 09:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('deal_findr', '0004_auto_20200419_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deal',
            name='productName',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
