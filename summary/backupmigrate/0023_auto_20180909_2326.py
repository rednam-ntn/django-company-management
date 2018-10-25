# Generated by Django 2.1 on 2018-09-09 23:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0022_auto_20180903_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='TBTCStatusLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(verbose_name='Cần sửa chữa')),
                ('date', models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày')),
            ],
            options={
                'verbose_name': 'Tình trạng',
                'verbose_name_plural': 'Tình trạng',
                'ordering': ['-date'],
            },
        ),
        migrations.AlterField(
            model_name='staff',
            name='d_in',
            field=models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày vào làm'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='dob',
            field=models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày sinh'),
        ),
        migrations.AlterField(
            model_name='tbtc',
            name='d_in',
            field=models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày mua'),
        ),
        migrations.AlterField(
            model_name='tbtc',
            name='d_out',
            field=models.DateField(blank=True, help_text='YYYY-MM-DD', null=True, verbose_name='Ngưng sử dụng Hoàn toàn'),
        ),
        migrations.AlterField(
            model_name='tbtcdocument',
            name='date_crt',
            field=models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày lập'),
        ),
        migrations.AlterField(
            model_name='tbtcdocument',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Project', verbose_name='Công trình'),
        ),
        migrations.AlterField(
            model_name='tbtcdocument',
            name='sponsor',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('deparment__short_text', 'BT'), ('deparment__short_text', 'TT'), _connector='OR'), ('d_out__isnull', True), models.Q(_negated=True, position__short_text='CN')), null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Staff', verbose_name='Người quản lý'),
        ),
        migrations.AlterField(
            model_name='tbtcmanage',
            name='d_receive',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_receive', to='summary.TBTCDocument', verbose_name='Văn bản giao ra công trình'),
        ),
        migrations.AlterField(
            model_name='tbtcmanage',
            name='d_return',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_return', to='summary.TBTCDocument', verbose_name='Văn bản trả về'),
        ),
        migrations.AlterField(
            model_name='tbvtdocument',
            name='date_crt',
            field=models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày lập'),
        ),
        migrations.AddField(
            model_name='tbtcstatuslog',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBTC', verbose_name='Thiết bị'),
        ),
    ]