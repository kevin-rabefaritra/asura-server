# Generated by Django 4.2.1 on 2024-01-05 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asura', '0012_alter_post_comments_count_alter_post_likes_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='postmedia',
            name='alt',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
    ]
