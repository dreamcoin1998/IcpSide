# Generated by Django 3.2.4 on 2021-07-02 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yonghu',
            name='avatar',
        ),
    ]
