from django.urls import reverse  # Generate URLs by reversing the URL patterns
from django.db import models
from django.core.validators import RegexValidator
# MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

import datetime as dt
# from dateutil.relativedelta import relativedelta
# from django.utils.translation import gettext_lazy as _

today = dt.date.today()


class AdminURLMixin(object):
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (
            content_type.app_label,
            content_type.model),
            args=(self.id,))

###########################################################


class Staff(models.Model):
    name = models.CharField(max_length=200, verbose_name='Họ và Tên')
    position = models.ForeignKey(
        'Position',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Chức vụ',
        )
    deparment = models.ForeignKey(
        'Deparment',
        to_field='id',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Bộ Phận',
        )
    office = models.BooleanField(
        default=False,
        verbose_name='Làm ở Văn phòng',
        )
    MaNV = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        verbose_name='Mã Nhân viên',
        )
    dob = models.DateField(
        null=True,
        default=dt.date.today,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày sinh',
        )
    d_in = models.DateField(
        null=True,
        default=dt.date.today,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày vào làm',
        )
    d_out = models.DateField(
        null=True,
        blank=True,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày nghỉ việc',
        )
    pros = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Chuyên môn',
        )
    cmnd = models.CharField(
        null=True,
        default='888888888',
        max_length=12,
        validators=[RegexValidator(regex=r'(^\d{9}$|^\d{12}$)')],
        help_text='CMND 9 số hoặc CCCD 12 số',
        verbose_name='Số CMND/CCCD',
        )
    certi = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Chứng chỉ',
        )
    pob = models.CharField(
        max_length=200,
        null=True,
        default='Sài Gòn',
        verbose_name='Nơi sinh',
        )
    hk = models.CharField(
        max_length=200,
        null=True,
        default='Sài Gòn',
        verbose_name='Hộ Khẩu',
        )
    address = models.CharField(
        max_length=200,
        null=True,
        default='Sài Gòn',
        verbose_name='Địa chỉ liên lạc',
        )
    tel = models.CharField(
        null=True,
        default='01234567890',
        max_length=11,
        validators=[RegexValidator(regex=r'(^0\d{9}$|^0\d{10}$)')],
        help_text='Di động 10 số hoặc 11 số',
        verbose_name='SĐT',
        )

    class Meta:
        ordering = ['id']
        verbose_name = "Nhân sự"
        verbose_name_plural = "Nhân sự"
        permissions = (("office_check", "Chấm công Văn phòng"),)

    def save(self,  *args, **kwargs):
        # get self.id
        super(Staff, self).save(*args, **kwargs)
        # AABB123
        if len(str(self.pk)) == 2:
            staff_id = (
                str(self.deparment.short_text) +
                str(self.position.short_text) + '0' +
                str(self.pk))
        elif len(str(self.pk)) == 1:
            staff_id = (
                str(self.deparment.short_text) +
                str(self.position.short_text) + '00' +
                str(self.pk))
        else:
            staff_id = (
                str(self.deparment.short_text) +
                str(self.position.short_text) +
                str(self.pk))
        self.__class__.objects.filter(pk=self.pk).update(MaNV=staff_id)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('staff_detail', args=[str(self.id)])


class Position(models.Model):
    position_text = models.CharField(max_length=100, verbose_name='Tên')
    short_text = models.CharField(
        max_length=2,
        null=True,
        help_text='2 ký tự',
        verbose_name='Mã',
        unique=True,
        )

    class Meta:
        verbose_name = 'Chức vụ'
        verbose_name_plural = 'Chức vụ'
        ordering = ['position_text']

    def __str__(self):
        return self.position_text


class Deparment(models.Model):
    name = models.CharField(max_length=100, verbose_name='Tên')
    short_text = models.CharField(
        max_length=2,
        null=True,
        help_text='2 ký tự',
        verbose_name='Mã',
        unique=True,
        )

    class Meta:
        verbose_name = 'Bộ phận'
        verbose_name_plural = 'Bộ phận'
        ordering = ['id']

    def __str__(self):
        return self.name

##################################


class Project(models.Model, AdminURLMixin):
    name = models.CharField(max_length=200, verbose_name='Công trình')
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Phạm vi công việc',
        )
    location = models.CharField(
        max_length=200,
        null=True,
        verbose_name='Địa điểm',
        )
    chief = models.ForeignKey(
        'Staff',
        to_field='id',
        limit_choices_to=(
            (models.Q(deparment=6) | models.Q(deparment=3)) &
            models.Q(d_out__isnull=True)
            ),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Chỉ huy Trưởng',
        )
    no_paid = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Số lần thanh toán',
        )
    STATUS_CHOICES = (
        ('DT', 'Đang Dự thầu'),
        ('CB', 'Đang Chuẩn bị'),
        ('TC', 'Đang Thi công'),
        ('HT', 'Đã Hoàn thành Thi công'),
        ('TL', 'Đã Thanh lý Hợp đồng'),
        )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='DT',
        verbose_name='Trạng thái',
        )
    note = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Ghi chú',
        )
    allowed_users = models.ManyToManyField(User)

    class Meta:
        ordering = ['status']
        verbose_name = "Công trình"
        verbose_name_plural = "Công trình"

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse('project_detail', args=[str(self.id)])

    def get_monthreport_url(self):
        return reverse('p_m_report', args=[str(self.id)])

    def get_check_url(self):
        return reverse('project_check', args=[str(self.id)])


class Allocation(models.Model):
    d_in = models.DateField(
        null=True,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày nhận phân công',
        )
    d_out = models.DateField(
        null=True,
        blank=True,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày hết hiệu lực phân công',
        )
    staff = models.ForeignKey(
        Staff,
        to_field='id',
        on_delete=models.PROTECT,
        limit_choices_to=(
            (models.Q(deparment=6) | models.Q(deparment=3)) &
            models.Q(d_out__isnull=True)
            ),
        null=True,
        verbose_name='Nhân sự',
        )
    project = models.ForeignKey(
        Project,
        to_field='id',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Công trình',
        )

    class Meta:
        ordering = ['project', '-d_in', 'd_out']
        verbose_name = 'Phân công Nhân sự'
        verbose_name_plural = 'Phân công Nhân sự'

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(
            self.id,
            self.staff,
            self.project,
            self.d_in,
            self.d_out,
            )


class DateLog(models.Model):
    date = models.DateField(null=True, blank=True, help_text='Date')
    staff = models.ForeignKey(
        Staff,
        to_field='id',
        on_delete=models.PROTECT,
        null=True
        )
    project = models.ForeignKey(
        Project,
        to_field='id',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        )
    shift1 = models.BooleanField(
        default=False,
        verbose_name='Ca sáng',
        )
    shift2 = models.BooleanField(
        default=False,
        verbose_name='Ca chiều',
        )
    shift3 = models.DurationField(
        null=True,
        blank=True,
        verbose_name='Tăng ca',
        )
    over9 = models.BooleanField(
        default=False,
        verbose_name='Trực đêm',
        )

    class Meta:
        ordering = ['-date', 'project']

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(
            self.id,
            self.date,
            self.staff,
            self.project
            )

###########################################################


class TBTC(models.Model, AdminURLMixin):
    MaTBTC = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        verbose_name='Mã TB',
        )
    type = models.ForeignKey(
        'TBTCType',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Tên',
        )
    brand = models.ForeignKey(
        'TBTCBrand',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Nhãn hiệu',
        )
    d_in = models.DateField(
        null=True,
        default=dt.date.today,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày mua',
        )
    d_out = models.DateField(
        null=True,
        blank=True,
        help_text='YYYY-MM-DD',
        verbose_name='Ngưng sử dụng Hoàn toàn',
        )

    class Meta:
        ordering = ['id']
        verbose_name = "Thiết bị Thi công"
        verbose_name_plural = "Thiết bị Thi công"
        permissions = (("manage_TBTC", "Quản lý TBTC"),)

    def save(self, *args, **kwargs):
        # get self pk (id)
        super(TBTC, self).save(*args, **kwargs)
        # AA1.A.001
        if len(str(self.pk)) == 2:
            TBTC_id = (
                str(self.type.short_text) + '.' +
                str(self.brand.short_text) + '.' + '0' +
                str(self.pk))
        elif len(str(self.pk)) == 1:
            TBTC_id = (
                str(self.type.short_text) + '.' +
                str(self.brand.short_text) + '.' + '00' +
                str(self.pk))
        else:
            TBTC_id = (
                str(self.type.short_text) + '.' +
                str(self.brand.short_text) + '.' +
                str(self.pk))
        self.__class__.objects.filter(pk=self.pk).update(MaTBTC=TBTC_id)

    def __str__(self):
        return '{0}, {1}, {2}'.format(
            self.id,
            self.type,
            self.brand,
            )

    def status(self):
        if TBTCStatusLog.objects.filter(unit=self).exists():
            tb_stt =\
             TBTCStatusLog.objects.filter(unit=self).first()
            date_conv = dt.datetime.strptime(str(tb_stt.date), '%Y-%m-%d')
            date_display = dt.datetime.strftime(date_conv, '%d/%m/%Y')
            if tb_stt.status is True:
                stt = 'Hư hỏng từ ngày ' + date_display
            else:
                stt = 'Tốt'
        else:
            stt = 'Tốt'
        return stt

    def get_manage_url(self):
        return reverse('tbtc_manage', args=[str(self.id)])


class TBTCDocument(models.Model):
    MaVB = models.CharField(
        null=True,
        max_length=100,
        verbose_name='Mã VB',
        unique=True,
        )
    name = models.CharField(max_length=200, verbose_name='Tên')
    project = models.ForeignKey(
        'Project',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Công trình',
        )
    sponsor = models.ForeignKey(
        'Staff',
        limit_choices_to=(
            (models.Q(deparment__short_text='BT') |
             models.Q(deparment__short_text='TT'))
            & models.Q(d_out__isnull=True)
            & ~models.Q(position__short_text='CN')
            ),
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Người quản lý',
        )
    date_crt = models.DateField(
        null=True,
        default=dt.date.today,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày lập',
        )

    class Meta:
        verbose_name = 'Văn bản TBTC'
        verbose_name_plural = 'Văn bản TBTC'
        ordering = ['-date_crt']

    def __str__(self):
        return self.MaVB


class TBTCManage(models.Model):
    unit = models.ForeignKey(
        'TBTC',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Thiết bị',
        )
    d_receive = models.ForeignKey(
        'TBTCDocument',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Văn bản giao ra công trình',
        related_name='d_receive',
        )
    d_return = models.ForeignKey(
        'TBTCDocument',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Văn bản Công trình giao trả',
        related_name='d_return',
        )

    class Meta:
        ordering = ['-d_return', 'd_receive']
        verbose_name = 'Phân bố TBTC'
        verbose_name_plural = 'Phân bố TBTC'

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(
            self.d_receive.project,
            self.d_receive.sponsor,
            self.d_receive,
            self.d_return,
            )


class TBTCStatusLog(models.Model):
    unit = models.ForeignKey(
        'TBTC',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Thiết bị',
        )
    status = models.BooleanField(verbose_name='Cần sửa chữa')
    date = models.DateField(
        null=True,
        default=dt.date.today,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày',
        )

    class Meta:
        verbose_name = 'Tình trạng TBTC'
        verbose_name_plural = 'Tình trạng TBTC'
        ordering = ['-id']

    def __str__(self):
        return '{0}, {1}'.format(
            self.status,
            self.date,
            )


class TBTCType(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tên TB')
    short_text = models.CharField(
        max_length=3,
        null=True,
        help_text='3 ký tự',
        verbose_name='Mã',
        unique=True,
        )

    class Meta:
        verbose_name = 'Loại TBTC'
        verbose_name_plural = 'Loại TBTC'
        ordering = ['name']

    def __str__(self):
        return self.name


class TBTCBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nhãn hiệu TBTC')
    short_text = models.CharField(
        max_length=1,
        null=True,
        help_text='1 ký tự',
        verbose_name='Mã',
        unique=True,
        )

    class Meta:
        verbose_name = 'Nhãn hiệu TBTC'
        verbose_name_plural = 'Nhãn hiệu TBTC'
        ordering = ['name']

    def __str__(self):
        return self.name


##################################


class TBVT(models.Model):
    MaTBVT = models.CharField(
        null=True,
        blank=True,
        max_length=12,
        verbose_name='Mã TBVT',
        )
    type = models.ForeignKey(
        'TBVTType',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Tên',
        )
    brand = models.ForeignKey(
        'TBVTBrand',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Nhãn hiệu',
        )
    unit_m = models.ForeignKey(
        'UnitMeasure',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Đơn vị',
        )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Số lượng')

    class Meta:
        verbose_name = 'Thiết bị - Vật tư'
        verbose_name_plural = 'Thiết bị - Vật tư'
        ordering = ['MaTBVT']
        permissions = (("manage_TBVT", "Quản lý TBVT"),)

    def save(self, *args, **kwargs):
        # get self pk (id)
        super(TBVT, self).save(*args, **kwargs)
        # AAAAA.AA.001
        if len(str(self.pk)) == 2:
            TBVT_id = (
                str(self.type.short_text) + '.' +
                str(self.brand.short_text) + '.' + '0' +
                str(self.pk))
        elif len(str(self.pk)) == 1:
            TBVT_id = (
                str(self.type.short_text) + '.' +
                str(self.brand.short_text) + '.' + '00' +
                str(self.pk))
        else:
            TBVT_id = (
                str(self.type.short_text) + '.' +
                str(self.brand.short_text) + '.' +
                str(self.pk))
        self.__class__.objects.filter(pk=self.pk).update(MaTBVT=TBVT_id)

    def __str__(self):
        return '{0}, {1}, {2}'.format(
            self.MaTBVT,
            self.quantity,
            self.unit_m,
            )


class TBVTDocument(models.Model):
    MaVB = models.CharField(
        null=True,
        max_length=100,
        verbose_name='Mã VB',
        unique=True,
        )
    name = models.CharField(max_length=200, verbose_name='Tên')
    project = models.ForeignKey(
        'Project',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Công trình',
        )
    sponsor = models.ForeignKey(
        'Staff',
        limit_choices_to=(
            (models.Q(deparment__short_text='BT') |
             models.Q(deparment__short_text='TT'))
            & models.Q(d_out__isnull=True)
            & ~models.Q(position__short_text='CN')
            ),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Người quản lý',
        )
    TBVT_CHOICES = (
        ('im', 'Nhập'),
        ('ex', 'Xuất'),
        )
    status = models.CharField(
        max_length=2,
        choices=TBVT_CHOICES,
        default='im',
        verbose_name='Nhập/Xuất',
        )
    date_crt = models.DateField(
        null=True,
        default=dt.date.today,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày lập',
        )

    class Meta:
        verbose_name = 'Văn bản TBVT'
        verbose_name_plural = 'Văn bản TBVT'
        ordering = ['-date_crt']

    def __str__(self):
        return self.MaVB


class TBVTManage(models.Model):
    document = models.ForeignKey(
        'TBVTDocument',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Văn bản',
        )
    unit = models.ForeignKey(
        'TBVT',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Vật tư',
        )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Số lượng')

    class Meta:
        verbose_name = 'Nhập/Xuất Vật tư'
        verbose_name_plural = 'Nhập/Xuất Vật tư'
        ordering = ['document']

    def __str__(self):
        return '{0}, {1}, {2}'.format(
            self.document,
            self.unit,
            self.quantity,
            )


class TBVTType(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tên Vật tư')
    short_text = models.CharField(
        max_length=5,
        null=True,
        help_text='Tối đa 5 ký tự',
        verbose_name='Mã',
        unique=True,
        )

    class Meta:
        verbose_name = 'Loại TBVT'
        verbose_name_plural = 'Loại TBVT'
        ordering = ['name']

    def __str__(self):
        return self.name


class TBVTBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nhãn hiệu TBVT')
    short_text = models.CharField(
        max_length=2,
        null=True,
        help_text='2 ký tự',
        verbose_name='Mã',
        unique=True,
        )

    class Meta:
        verbose_name = 'Nhãn hiệu TBVT'
        verbose_name_plural = 'Nhãn hiệu TBVT'
        ordering = ['name']

    def __str__(self):
        return self.name


class UnitMeasure(models.Model):
    name = models.CharField(max_length=100, verbose_name='Đơn vị')

    class Meta:
        verbose_name = 'Đơn vị'
        verbose_name_plural = 'Đơn vị'
        ordering = ['name']

    def __str__(self):
        return self.name
