# Generated by Django 2.2.24 on 2021-09-08 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Addkeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(blank=True, default=None, max_length=30)),
                ('keyString', models.CharField(max_length=255)),
                ('usedTime', models.DateTimeField(blank=True, default=None)),
            ],
        ),
    ]
