# Generated by Django 3.2.4 on 2021-07-04 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0004_alter_verificationcode_update_time'),
        ('access_log', '0002_accesslog_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='auth_user.yonghu'),
        ),
    ]
