# Generated by Django 4.2.1 on 2023-12-02 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asura', '0009_user_bio_user_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='type',
            field=models.CharField(choices=[('access', 'Access token'), ('refresh', 'Refresh token')], default='access', max_length=20, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='token',
            name='key',
            field=models.CharField(max_length=1000, primary_key=True, serialize=False, verbose_name='Key'),
        ),
    ]
