# Generated by Django 2.1 on 2018-09-03 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0020_auto_20180903_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbtcdocument',
            name='status',
        ),
    ]
