# Generated by Django 2.1 on 2018-09-03 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0019_auto_20180903_1707'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Document',
            new_name='TBTCDocument',
        ),
        migrations.AlterField(
            model_name='tbvtmanage',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBVTDocument', verbose_name='Văn bản'),
        ),
    ]