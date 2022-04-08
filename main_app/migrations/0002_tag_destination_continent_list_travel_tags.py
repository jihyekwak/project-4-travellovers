# Generated by Django 4.0.3 on 2022-04-08 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='destination',
            name='continent',
            field=models.CharField(choices=[('Europe', 'Europe'), ('Oceania', 'Oceania'), ('Africa', 'Africa'), ('Antarctica', 'Antarctica'), ('North America', 'North America'), ('Asia', 'Asia'), ('Sourth America', 'South America')], max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('To Do List', 'To Do List'), ('Packing List', 'Packing List'), ('Check List', 'Check List')], max_length=20)),
                ('item', models.CharField(max_length=250)),
                ('priority', models.CharField(choices=[('High', 'High'), ('Low', 'Low'), ('None', 'None'), ('Medium', 'Medium')], max_length=20)),
                ('is_completed', models.BooleanField(default=False)),
                ('due_date', models.DateField(blank=True)),
                ('travel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lists', to='main_app.travel')),
            ],
        ),
        migrations.AddField(
            model_name='travel',
            name='tags',
            field=models.ManyToManyField(to='main_app.tag'),
        ),
    ]