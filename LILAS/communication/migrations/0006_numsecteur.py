# Generated by Django 2.1.3 on 2019-05-03 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0005_numexterieur'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumSecteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_elts', models.CharField(max_length=4)),
                ('id_lilas', models.CharField(max_length=4)),
                ('numero', models.CharField(max_length=15)),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
    ]
