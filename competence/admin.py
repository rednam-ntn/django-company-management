from django.contrib import admin
from .models import AbilityType, QuestionDetail, AnswerDetail, AbilityTest,\
 QADetail, FormVersion


class AbilityTestInline(admin.TabularInline):
    model = AbilityTest
    extra = 0


class QADetailInline(admin.TabularInline):
    model = QADetail
    extra = 0


class AnswerDetailInline(admin.TabularInline):
    model = AnswerDetail
    extra = 0


class QuestionDetailInline(admin.TabularInline):
    model = QuestionDetail
    extra = 0


@admin.register(AbilityType)
class AbilityTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'short_text')
    list_display_links = ['text', 'short_text']
    inlines = [QuestionDetailInline]


@admin.register(QuestionDetail)
class QuestionDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'text', 'code')
    list_display_links = ['type', 'text', 'code']
    inlines = [AnswerDetailInline]


@admin.register(AnswerDetail)
class AnswerDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'rank', 'question')
    list_display_links = ['text', 'rank', 'question']


@admin.register(AbilityTest)
class AbilityTestAdmin(admin.ModelAdmin):
    list_display = ('staff', 'sponsor', 'date', 'result')
    list_display_links = ['staff', 'sponsor', 'date', 'result']
    inlines = [QADetailInline]


@admin.register(FormVersion)
class FormVersionAdmin(admin.ModelAdmin):
    list_display = ('construct',)
    list_display_links = ['construct']
    inlines = [AbilityTestInline]


@admin.register(QADetail)
class QADetailAdmin(admin.ModelAdmin):
    list_display = ('test', 'question', 'answer', 'num_order')
    list_display_links = ['test', 'question', 'answer', 'num_order']
