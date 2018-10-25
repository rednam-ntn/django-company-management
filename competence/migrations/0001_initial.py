# Generated by Django 2.1 on 2018-10-18 13:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('summary', '0008_auto_20181012_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbilityTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày đánh giá')),
                ('result', models.SmallIntegerField(null=True, verbose_name='Bậc năng lực')),
                ('sponsor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sponsor', to='summary.Staff', verbose_name='Người đánh giá')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='staff', to='summary.Staff', verbose_name='Nhân sự được đánh giá')),
            ],
            options={
                'verbose_name': 'Đánh giá năng lực',
                'verbose_name_plural': 'Đánh giá năng lực',
                'ordering': ['date'],
                'permissions': (('abi_test', 'Đánh giá nhân sự'),),
            },
        ),
        migrations.CreateModel(
            name='AbilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='Mô tả')),
                ('short_text', models.CharField(help_text='3 ký tự', max_length=3, null=True, unique=True, verbose_name='Mã')),
            ],
            options={
                'verbose_name': 'Mục Đánh giá',
                'verbose_name_plural': 'Mục Đánh giá',
            },
        ),
        migrations.CreateModel(
            name='AnswerDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='Mô tả')),
                ('rank', models.SmallIntegerField(null=True, verbose_name='Thang điểm')),
            ],
            options={
                'verbose_name': 'Bậc Đánh giá',
                'verbose_name_plural': 'Bậc Đánh giá',
            },
        ),
        migrations.CreateModel(
            name='QADetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='competence.AnswerDetail', verbose_name='Thang điểm')),
            ],
            options={
                'verbose_name': 'Chi tiết đánh giá',
                'verbose_name_plural': 'Chi tiết đánh giá',
            },
        ),
        migrations.CreateModel(
            name='QuestionDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='Tiểu mục ĐG')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='competence.AbilityType', verbose_name='Mục ĐG')),
            ],
            options={
                'verbose_name': 'Tiểu mục Đánh giá',
                'verbose_name_plural': 'Tiểu mục Đánh giá',
            },
        ),
        migrations.AddField(
            model_name='qadetail',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='competence.QuestionDetail', verbose_name='Câu hỏi'),
        ),
        migrations.AddField(
            model_name='qadetail',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='competence.AbilityTest', verbose_name='Bài đánh giá'),
        ),
        migrations.AddField(
            model_name='answerdetail',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='competence.QuestionDetail', verbose_name='Câu hỏi'),
        ),
    ]