# Generated by Django 4.2.1 on 2024-01-18 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asura', '0013_post_tags_postmedia_alt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postreaction',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_post_reactions', to='asura.user'),
        ),
    ]
