# Generated by Django 3.1.5 on 2021-01-22 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userInterface', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='is_remind_details',
        ),
        migrations.AddField(
            model_name='students',
            name='password',
            field=models.CharField(default=1, max_length=256, verbose_name='密码'),
            preserve_default=False,
        ),
    ]
