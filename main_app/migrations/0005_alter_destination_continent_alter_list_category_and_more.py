# Generated by Django 4.0.3 on 2022-04-09 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_destination_continent_alter_list_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='continent',
            field=models.CharField(choices=[('North America', 'North America'), ('Europe', 'Europe'), ('Africa', 'Africa'), ('Sourth America', 'South America'), ('Oceania', 'Oceania'), ('Asia', 'Asia'), ('Antarctica', 'Antarctica')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='category',
            field=models.CharField(choices=[('Check List', 'Check List'), ('To Do List', 'To Do List'), ('Packing List', 'Packing List')], max_length=20),
        ),
        migrations.AlterField(
            model_name='list',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='priority',
            field=models.CharField(blank=True, choices=[('Low', 'Low'), ('None', 'None'), ('High', 'High'), ('Medium', 'Medium')], max_length=20),
        ),
    ]
