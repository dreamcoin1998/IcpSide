# Generated by Django 3.2.4 on 2021-06-25 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=6)),
                ('product_type_id', models.IntegerField()),
                ('product_detail', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField()),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_user.user')),
            ],
        ),
    ]
