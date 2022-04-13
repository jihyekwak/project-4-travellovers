# Generated by Django 4.0.4 on 2022-04-13 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_destination_continent_alter_list_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='continent',
            field=models.CharField(choices=[('Africa', 'Africa'), ('Antarctica', 'Antarctica'), ('Sourth America', 'South America'), ('Oceania', 'Oceania'), ('Europe', 'Europe'), ('North America', 'North America'), ('Asia', 'Asia')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='list',
            name='priority',
            field=models.CharField(blank=True, choices=[('None', 'None'), ('Medium', 'Medium'), ('Low', 'Low'), ('High', 'High')], max_length=20),
        ),
    ]
