# Generated by Django 2.1 on 2018-09-26 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbtcdocument',
            name='project',
            field=models.ForeignKey(help_text='Nếu trả Thiết bị về Kho, vui lòng để tên nơi trả', null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Project', verbose_name='Công trình'),
        ),
    ]