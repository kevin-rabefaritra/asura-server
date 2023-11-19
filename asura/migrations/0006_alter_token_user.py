# Generated by Django 4.2.1 on 2023-06-04 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asura', '0005_alter_userconversation_conversation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='asura.user', verbose_name='User'),
        ),
    ]