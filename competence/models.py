from django.db import models
from summary.models import Staff
import datetime as dt


class AbilityType(models.Model):
    text = models.CharField(max_length=100, verbose_name='Mô tả')
    short_text = models.CharField(
        unique=True, null=True,
        max_length=3, help_text='3 ký tự',
        verbose_name='Mã')

    class Meta:
        verbose_name = "Mục Đánh giá"
        verbose_name_plural = "Mục Đánh giá"

    def __str__(self):
        return self.text


class QuestionDetail(models.Model):
    text = models.CharField(max_length=100, verbose_name='Nội dung')
    description = models.CharField(
        null=True, blank=True,
        max_length=200, verbose_name='Mô tả')
    type = models.ForeignKey(
        'AbilityType', to_field='id', null=True,
        on_delete=models.PROTECT,
        verbose_name='Mục ĐG',)
    code = models.CharField(null=True, blank=True, max_length=10,
                            verbose_name='Mã mục')

    class Meta:
        verbose_name = "Tiểu mục Đánh giá"
        verbose_name_plural = "Tiểu mục Đánh giá"

    def __str__(self):
        return '{0}, {1}'.format(self.type, self.text)


class AnswerDetail(models.Model):
    text = models.CharField(max_length=200, verbose_name='Mô tả')
    rank = models.SmallIntegerField(null=True, verbose_name='Điểm')
    question = models.ForeignKey(
        'QuestionDetail', to_field='id', null=True,
        on_delete=models.PROTECT,
        verbose_name='Câu hỏi')

    class Meta:
        verbose_name = "Bậc Đánh giá"
        verbose_name_plural = "Bậc Đánh giá"

    def __str__(self):
        return '{0}, {1}'.format(self.question, self.rank)

###########################################################


class AbilityTest(models.Model):
    form_version = models.ForeignKey(
        'FormVersion', to_field='id', null=True,
        on_delete=models.PROTECT, verbose_name='Form',
        )
    staff = models.ForeignKey(
        Staff, to_field='id', null=True,
        on_delete=models.PROTECT,
        verbose_name='Nhân sự được đánh giá',
        related_name='staff',
        # limit_choices_to=(
        #    (models.Q(deparment=6) | models.Q(deparment=3)) &
        #    models.Q(d_out__isnull=True)),
        )
    sponsor = models.ForeignKey(
        Staff, to_field='id', null=True,
        on_delete=models.PROTECT,
        verbose_name='Người đánh giá',
        related_name='sponsor',
        )
    date = models.DateField(
        default=dt.date.today, null=True,
        help_text='YYYY-MM-DD',
        verbose_name='Ngày đánh giá',
        )
    result = models.SmallIntegerField(
        null=True, blank=True,
        verbose_name='Bậc năng lực',)

    class Meta:
        ordering = ['date']
        verbose_name = "Đánh giá năng lực"
        verbose_name_plural = "Đánh giá năng lực"
        permissions = (("abi_test", "Đánh giá nhân sự"),)

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(
            self.id, self.staff, self.sponsor, self.date)


class FormVersion(models.Model):
    construct = models.CharField(null=True, blank=True, max_length=200,
                                 verbose_name='Form')

    def __str__(self):
        return self.construct


class QADetail(models.Model):
    test = models.ForeignKey(
        'AbilityTest', to_field='id', null=True,
        on_delete=models.PROTECT,
        verbose_name='Bài đánh giá',
        )
    question = models.ForeignKey(
        'QuestionDetail', to_field='id', null=True,
        on_delete=models.PROTECT,
        verbose_name='Câu hỏi',
        )
    answer = models.ForeignKey(
        'AnswerDetail', to_field='id', null=True,
        on_delete=models.PROTECT,
        verbose_name='Thang điểm',
        )
    num_order = models.SmallIntegerField(null=True, blank=True,
                                         verbose_name='STT')

    class Meta:
        ordering = ['num_order']
        verbose_name = "Chi tiết đánh giá"
        verbose_name_plural = "Chi tiết đánh giá"

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(
            self.test.staff, self.test.date, self.question, self.answer)
