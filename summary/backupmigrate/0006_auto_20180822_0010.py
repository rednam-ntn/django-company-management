# Generated by Django 2.0.5 on 2018-08-22 00:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0005_auto_20180822_0008'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tbtcmanage',
            options={'ordering': ['project'], 'verbose_name': 'Phân bố TBTC', 'verbose_name_plural': 'Phân bố TBTC'},
        ),
    ]