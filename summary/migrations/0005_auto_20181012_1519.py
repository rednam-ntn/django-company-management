# Generated by Django 2.1 on 2018-10-12 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0004_auto_20181007_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datelog',
            name='in1',
        ),
        migrations.RemoveField(
            model_name='datelog',
            name='in2',
        ),
        migrations.RemoveField(
            model_name='datelog',
            name='in3',
        ),
        migrations.RemoveField(
            model_name='datelog',
            name='out1',
        ),
        migrations.RemoveField(
            model_name='datelog',
            name='out2',
        ),
        migrations.RemoveField(
            model_name='datelog',
            name='out3',
        ),
        migrations.AddField(
            model_name='datelog',
            name='shift_1',
            field=models.BooleanField(default=False, verbose_name='Ca sáng'),
        ),
        migrations.AddField(
            model_name='datelog',
            name='shift_2',
            field=models.BooleanField(default=False, verbose_name='Ca chiều'),
        ),
        migrations.AddField(
            model_name='datelog',
            name='shift_3',
            field=models.DurationField(blank=True, null=True, verbose_name='Tăng ca'),
        ),
        migrations.AlterField(
            model_name='datelog',
            name='over9',
            field=models.TimeField(blank=True, null=True, verbose_name='Trực đêm'),
        ),
    ]
