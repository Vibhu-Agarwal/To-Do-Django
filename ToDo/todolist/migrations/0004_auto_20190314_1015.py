# Generated by Django 2.1.7 on 2019-03-14 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_auto_20190314_0617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todolist',
            old_name='content',
            new_name='description',
        ),
    ]
