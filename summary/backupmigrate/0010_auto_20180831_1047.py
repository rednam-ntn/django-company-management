# Generated by Django 2.1 on 2018-08-31 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0009_auto_20180831_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbvtbrand',
            name='short_text',
            field=models.CharField(help_text='2 ký tự', max_length=2, null=True, unique=True, verbose_name='Mã'),
        ),
    ]
