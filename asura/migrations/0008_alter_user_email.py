# Generated by Django 4.2.1 on 2023-10-23 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asura', '0007_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]