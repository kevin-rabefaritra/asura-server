# Generated by Django 4.2.1 on 2023-06-03 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asura', '0004_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconversation',
            name='conversation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='asura.conversation'),
        ),
    ]
