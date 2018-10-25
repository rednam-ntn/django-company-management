# Generated by Django 2.1 on 2018-08-31 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0012_auto_20180831_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='sponsor',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('deparment', 6), ('deparment', 3), _connector='OR'), ('d_out__isnull', True)), null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Staff', verbose_name='Người quản lý'),
        ),
    ]
