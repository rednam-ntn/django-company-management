# Generated by Django 2.1 on 2018-10-07 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0003_auto_20181007_1611'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tbvt',
            options={'ordering': ['MaTBVT'], 'permissions': (('manage_TBVT', 'Quản lý TBVT'),), 'verbose_name': 'Thiết bị - Vật tư', 'verbose_name_plural': 'Thiết bị - Vật tư'},
        ),
    ]
