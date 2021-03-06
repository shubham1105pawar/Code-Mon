# Generated by Django 3.0.6 on 2020-05-31 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Problem_Name', models.CharField(max_length=50, unique=True)),
                ('Problem_Description', models.TextField()),
                ('Problem_Tags', models.TextField()),
                ('Problem', models.TextField()),
                ('Problem_Setter', models.CharField(max_length=50, unique=True)),
                ('Total_submission', models.IntegerField(default=0)),
                ('Total_Accepted', models.IntegerField(default=0)),
                ('Problem_level', models.CharField(max_length=8)),
                ('Language', models.CharField(max_length=15)),
            ],
        ),
    ]
