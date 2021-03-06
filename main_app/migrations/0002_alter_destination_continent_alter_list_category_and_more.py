# Generated by Django 4.0.4 on 2022-04-13 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='continent',
            field=models.CharField(choices=[('Africa', 'Africa'), ('Sourth America', 'South America'), ('Europe', 'Europe'), ('Oceania', 'Oceania'), ('Asia', 'Asia'), ('North America', 'North America'), ('Antarctica', 'Antarctica')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='category',
            field=models.CharField(choices=[('To Confirm List', 'To Confirm List'), ('To Do List', 'To Do List'), ('Packing List', 'Packing List')], max_length=20),
        ),
        migrations.AlterField(
            model_name='list',
            name='priority',
            field=models.CharField(blank=True, choices=[('High', 'High'), ('Low', 'Low'), ('Medium', 'Medium'), ('None', 'None')], max_length=20),
        ),
    ]
