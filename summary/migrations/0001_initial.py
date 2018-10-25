# Generated by Django 2.1 on 2018-09-20 12:53

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import summary.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_in', models.DateField(help_text='YYYY-MM-DD', null=True, verbose_name='Ngày nhận phân công')),
                ('d_out', models.DateField(blank=True, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày hết hiệu lực phân công')),
            ],
            options={
                'verbose_name': 'Phân công Nhân sự',
                'verbose_name_plural': 'Phân công Nhân sự',
                'ordering': ['project', '-d_in', 'd_out'],
            },
        ),
        migrations.CreateModel(
            name='DateLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, help_text='Date', null=True)),
                ('in1', models.TimeField(blank=True, null=True)),
                ('out1', models.TimeField(blank=True, null=True)),
                ('in2', models.TimeField(blank=True, null=True)),
                ('out2', models.TimeField(blank=True, null=True)),
                ('in3', models.TimeField(blank=True, null=True)),
                ('out3', models.TimeField(blank=True, null=True)),
                ('over9', models.TimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-date', 'project'],
            },
        ),
        migrations.CreateModel(
            name='Deparment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Tên')),
                ('short_text', models.CharField(help_text='2 ký tự', max_length=2, null=True, unique=True, verbose_name='Mã')),
            ],
            options={
                'verbose_name': 'Bộ phận',
                'verbose_name_plural': 'Bộ phận',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_text', models.CharField(max_length=100, verbose_name='Tên')),
                ('short_text', models.CharField(help_text='2 ký tự', max_length=2, null=True, unique=True, verbose_name='Mã')),
            ],
            options={
                'verbose_name': 'Chức vụ',
                'verbose_name_plural': 'Chức vụ',
                'ordering': ['position_text'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Công trình')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Phạm vi công việc')),
                ('location', models.CharField(max_length=200, null=True, verbose_name='Địa điểm')),
                ('no_paid', models.PositiveIntegerField(blank=True, null=True, verbose_name='Số lần thanh toán')),
                ('status', models.CharField(choices=[('DT', 'Đang Dự thầu'), ('CB', 'Đang Chuẩn bị'), ('TC', 'Đang Thi công'), ('HT', 'Đã Hoàn thành Thi công'), ('TL', 'Đã Thanh lý Hợp đồng')], default='DT', max_length=2, verbose_name='Trạng thái')),
                ('note', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ghi chú')),
                ('allowed_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Công trình',
                'verbose_name_plural': 'Công trình',
                'ordering': ['status'],
            },
            bases=(models.Model, summary.models.AdminURLMixin),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Họ và Tên')),
                ('office', models.BooleanField(default=False, verbose_name='Làm ở Văn phòng')),
                ('MaNV', models.CharField(blank=True, max_length=10, null=True, verbose_name='Mã Nhân viên')),
                ('dob', models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày sinh')),
                ('d_in', models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày vào làm')),
                ('d_out', models.DateField(blank=True, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày nghỉ việc')),
                ('pros', models.CharField(blank=True, max_length=100, null=True, verbose_name='Chuyên môn')),
                ('cmnd', models.CharField(default='888888888', help_text='CMND 9 số hoặc CCCD 12 số', max_length=12, null=True, validators=[django.core.validators.RegexValidator(regex='(^\\d{9}$|^\\d{12}$)')], verbose_name='Số CMND/CCCD')),
                ('certi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Chứng chỉ')),
                ('pob', models.CharField(default='Sài Gòn', max_length=200, null=True, verbose_name='Nơi sinh')),
                ('hk', models.CharField(default='Sài Gòn', max_length=200, null=True, verbose_name='Hộ Khẩu')),
                ('address', models.CharField(default='Sài Gòn', max_length=200, null=True, verbose_name='Địa chỉ liên lạc')),
                ('tel', models.CharField(default='01234567890', help_text='Di động 10 số hoặc 11 số', max_length=11, null=True, validators=[django.core.validators.RegexValidator(regex='(^0\\d{9}$|^0\\d{10}$)')], verbose_name='SĐT')),
                ('deparment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Deparment', verbose_name='Bộ Phận')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Position', verbose_name='Chức vụ')),
            ],
            options={
                'verbose_name': 'Nhân sự',
                'verbose_name_plural': 'Nhân sự',
                'ordering': ['id'],
                'permissions': (('office_check', 'Chấm công Văn phòng'),),
            },
        ),
        migrations.CreateModel(
            name='TBTC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MaTBTC', models.CharField(blank=True, max_length=10, null=True, verbose_name='Mã TB')),
                ('d_in', models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày mua')),
                ('d_out', models.DateField(blank=True, help_text='YYYY-MM-DD', null=True, verbose_name='Ngưng sử dụng Hoàn toàn')),
            ],
            options={
                'verbose_name': 'Thiết bị Thi công',
                'verbose_name_plural': 'Thiết bị Thi công',
                'ordering': ['id'],
            },
            bases=(models.Model, summary.models.AdminURLMixin),
        ),
        migrations.CreateModel(
            name='TBTCBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nhãn hiệu TBTC')),
                ('short_text', models.CharField(help_text='1 ký tự', max_length=1, null=True, unique=True, verbose_name='Mã')),
            ],
            options={
                'verbose_name': 'Nhãn hiệu TBTC',
                'verbose_name_plural': 'Nhãn hiệu TBTC',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TBTCDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MaVB', models.CharField(max_length=100, null=True, unique=True, verbose_name='Mã VB')),
                ('name', models.CharField(max_length=200, verbose_name='Tên')),
                ('date_crt', models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày lập')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Project', verbose_name='Công trình')),
                ('sponsor', models.ForeignKey(limit_choices_to=models.Q(models.Q(('deparment__short_text', 'BT'), ('deparment__short_text', 'TT'), _connector='OR'), ('d_out__isnull', True), models.Q(_negated=True, position__short_text='CN')), null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Staff', verbose_name='Người quản lý')),
            ],
            options={
                'verbose_name': 'Văn bản TBTC',
                'verbose_name_plural': 'Văn bản TBTC',
                'ordering': ['-date_crt'],
            },
        ),
        migrations.CreateModel(
            name='TBTCManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_receive', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_receive', to='summary.TBTCDocument', verbose_name='Văn bản giao ra công trình')),
                ('d_return', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='d_return', to='summary.TBTCDocument', verbose_name='Văn bản Công trình giao trả')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBTC', verbose_name='Thiết bị')),
            ],
            options={
                'verbose_name': 'Phân bố TBTC',
                'verbose_name_plural': 'Phân bố TBTC',
                'ordering': ['-d_return', 'd_receive'],
            },
        ),
        migrations.CreateModel(
            name='TBTCStatusLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(verbose_name='Cần sửa chữa')),
                ('date', models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBTC', verbose_name='Thiết bị')),
            ],
            options={
                'verbose_name': 'Tình trạng',
                'verbose_name_plural': 'Tình trạng',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TBTCType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Tên TB')),
                ('short_text', models.CharField(help_text='3 ký tự', max_length=3, null=True, unique=True, verbose_name='Mã')),
            ],
            options={
                'verbose_name': 'Loại TBTC',
                'verbose_name_plural': 'Loại TBTC',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TBVT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MaTBVT', models.CharField(blank=True, max_length=12, null=True, verbose_name='Mã TBVT')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Số lượng')),
            ],
            options={
                'verbose_name': 'Thiết bị - Vật tư',
                'verbose_name_plural': 'Thiết bị - Vật tư',
                'ordering': ['MaTBVT'],
            },
        ),
        migrations.CreateModel(
            name='TBVTBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nhãn hiệu TBVT')),
                ('short_text', models.CharField(help_text='2 ký tự', max_length=2, null=True, unique=True, verbose_name='Mã')),
            ],
            options={
                'verbose_name': 'Nhãn hiệu TBVT',
                'verbose_name_plural': 'Nhãn hiệu TBVT',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TBVTDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MaVB', models.CharField(max_length=100, null=True, unique=True, verbose_name='Mã VB')),
                ('name', models.CharField(max_length=200, verbose_name='Tên')),
                ('status', models.CharField(choices=[('im', 'Nhập'), ('ex', 'Xuất')], default='im', max_length=2, verbose_name='Nhập/Xuất')),
                ('date_crt', models.DateField(default=datetime.date.today, help_text='YYYY-MM-DD', null=True, verbose_name='Ngày lập')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Project', verbose_name='Công trình')),
                ('sponsor', models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('deparment__short_text', 'BT'), ('deparment__short_text', 'TT'), _connector='OR'), ('d_out__isnull', True), models.Q(_negated=True, position__short_text='CN')), null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Staff', verbose_name='Người quản lý')),
            ],
            options={
                'verbose_name': 'Văn bản TBVT',
                'verbose_name_plural': 'Văn bản TBVT',
                'ordering': ['-date_crt'],
            },
        ),
        migrations.CreateModel(
            name='TBVTManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Số lượng')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBVTDocument', verbose_name='Văn bản')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBVT', verbose_name='Vật tư')),
            ],
            options={
                'verbose_name': 'Nhập/Xuất Vật tư',
                'verbose_name_plural': 'Nhập/Xuất Vật tư',
                'ordering': ['document'],
            },
        ),
        migrations.CreateModel(
            name='TBVTType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Tên Vật tư')),
                ('short_text', models.CharField(help_text='Tối đa 5 ký tự', max_length=5, null=True, unique=True, verbose_name='Mã')),
            ],
            options={
                'verbose_name': 'Loại TBVT',
                'verbose_name_plural': 'Loại TBVT',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UnitMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Đơn vị')),
            ],
            options={
                'verbose_name': 'Đơn vị',
                'verbose_name_plural': 'Đơn vị',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='tbvt',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBVTBrand', verbose_name='Nhãn hiệu'),
        ),
        migrations.AddField(
            model_name='tbvt',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBVTType', verbose_name='Tên'),
        ),
        migrations.AddField(
            model_name='tbvt',
            name='unit_m',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.UnitMeasure', verbose_name='Đơn vị'),
        ),
        migrations.AddField(
            model_name='tbtc',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBTCBrand', verbose_name='Nhãn hiệu'),
        ),
        migrations.AddField(
            model_name='tbtc',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.TBTCType', verbose_name='Tên'),
        ),
        migrations.AddField(
            model_name='project',
            name='chief',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('deparment', 6), ('deparment', 3), _connector='OR'), ('d_out__isnull', True)), null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Staff', verbose_name='Chỉ huy Trưởng'),
        ),
        migrations.AddField(
            model_name='datelog',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Project'),
        ),
        migrations.AddField(
            model_name='datelog',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Staff'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Project', verbose_name='Công trình'),
        ),
        migrations.AddField(
            model_name='allocation',
            name='staff',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('deparment', 6), ('deparment', 3), _connector='OR'), ('d_out__isnull', True)), null=True, on_delete=django.db.models.deletion.PROTECT, to='summary.Staff', verbose_name='Nhân sự'),
        ),
    ]