# Generated by Django 3.0.6 on 2020-06-02 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Code_sh', '0003_solved'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solved',
            old_name='user',
            new_name='user_name',
        ),
    ]