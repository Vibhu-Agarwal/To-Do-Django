# Generated by Django 2.1.7 on 2019-03-14 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField(blank=True)),
                ('created', models.DateField(default='2019-03-14')),
                ('due_date', models.DateField(default='2019-03-14')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.Category')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]