# Generated by Django 2.1.3 on 2019-04-24 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configSalle', '0002_auto_20190424_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uce',
            name='configurationSalle',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='configSalle.ConfigurationSalle'),
        ),
    ]
