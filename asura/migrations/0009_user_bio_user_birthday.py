# Generated by Django 4.2.1 on 2023-11-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asura', '0008_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default=None, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=None, null=True),
        ),
    ]
