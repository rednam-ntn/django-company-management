# Generated by Django 2.1 on 2018-10-19 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competence', '0006_remove_abilitytest_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiondetail',
            name='code',
            field=models.SmallIntegerField(null=True, verbose_name='Mã mục'),
        ),
    ]
