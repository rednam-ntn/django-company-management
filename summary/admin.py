from django.contrib import admin

from .models import Position, Deparment, Staff, Project, Allocation, DateLog,\
 TBTC, TBTCType, TBTCBrand, TBTCManage, TBTCDocument, TBTCStatusLog,\
 TBVTManage, TBVT, TBVTType, TBVTBrand, UnitMeasure, TBVTDocument

from django import forms

###################################################################
# Form clean


class StaffAdminForm(forms.ModelForm):
    model = Staff

    def clean(self):
        if self.cleaned_data['d_out'] is not None:
            if self.cleaned_data['d_in'] > self.cleaned_data['d_out']:
                raise forms.ValidationError('Ngày nghỉ phải sau ngày vào')
            return self.cleaned_data


class TBTCAdminForm(forms.ModelForm):
    model = TBTC

    def clean(self):
        if self.cleaned_data['d_out'] is not None:
            if self.cleaned_data['d_in'] > self.cleaned_data['d_out']:
                raise forms.ValidationError('Ngày ngưng sử dụng phải sau\
                                            ngày mua')
            return self.cleaned_data


class TBTCDocumentAdminForm(forms.ModelForm):
    model = TBTCDocument

    def clean(self):  # validate for sponsor in project or GS
        if self.cleaned_data['sponsor'] is None:
            raise forms.ValidationError('Thiếu Người quản lý')
        elif self.cleaned_data['sponsor'] is not None and\
                self.cleaned_data['project'] is not None:
            p_allos = Allocation.objects.filter(
                project=self.cleaned_data['project'],
                d_out__isnull=True)
            staffs = list()
            for p_allo in p_allos:
                staffs.append(p_allo.staff)

            if self.cleaned_data['sponsor'] not in staffs and\
                    self.cleaned_data['sponsor'].position.short_text != 'CN':
                raise forms.ValidationError('Người quản lý phải thuộc phạm vi \
                                            phân công của công trình hoặc \
                                            phải là giám sát trở lên')
            return self.cleaned_data

###################################################################
# Inlines display


class ProjetInline(admin.TabularInline):
    model = Project
    extra = 0


class StaffInline(admin.TabularInline):
    model = Staff
    extra = 0


class AllocationInline(admin.TabularInline):
    model = Allocation
    extra = 0

#######################################


class TBTCReceiveInline(admin.TabularInline):
    model = TBTCManage
    extra = 0
    fk_name = "d_receive"
    fields = ('unit',)
    verbose_name = 'Thiết bị Bàn giao'


class TBTCReturnInline(admin.TabularInline):
    model = TBTCManage
    extra = 0
    fk_name = "d_return"
    fields = ('unit', 'd_receive')
    readonly_fields = ('d_receive',)
    verbose_name = 'Thiết bị Nhập kho'


class TBTCManageInline(admin.TabularInline):
    model = TBTCManage
    extra = 1
    readonly_fields = ('d_receive_project', 'd_receive_sponsor',
                       'd_receive_date_crt', 'd_return_project',
                       'd_return_sponsor', 'd_return_date_crt')
    fieldsets = (
        ('Văn bản Bàn giao Công trình', {'fields': (
            ('d_receive'), ('d_receive_project'),
            ('d_receive_sponsor'), ('d_receive_date_crt')
            )}),
        ('Vản bản Công trình trả về', {'fields': (
            ('d_return'), ('d_return_project'),
            ('d_return_sponsor'), ('d_return_date_crt')
            )}),
        )

    def d_receive_project(self, obj):
        return obj.d_receive.project
    d_receive_project.short_description = 'Công trình hiện tại'

    def d_receive_sponsor(self, obj):
        return obj.d_receive.sponsor
    d_receive_sponsor.short_description = 'Người quản lý hiện tại'

    def d_receive_date_crt(self, obj):
        return obj.d_receive.date_crt
    d_receive_date_crt.short_description = 'Ngày giao ra Công trình'

    def d_return_project(self, obj):
        return obj.d_return.project
    d_return_project.short_description = 'Nơi tiếp nhận tiếp theo'
    d_return_project.help_text = 'Nếu trả về kho, vui lòng để tên\
     công trình hiện tại'

    def d_return_sponsor(self, obj):
        return obj.d_return.sponsor
    d_return_sponsor.short_description = 'Người tiếp nhận'

    def d_return_date_crt(self, obj):
        return obj.d_return.date_crt
    d_return_date_crt.short_description = 'Ngày Công trình giao trả'


class TBTCDocumentReadOnlyInline(admin.TabularInline):
    model = TBTCDocument
    extra = 0
    max_num = 0
    readonly_fields = ('MaVB', 'name', 'sponsor', 'date_crt')
    can_delete = False


class TBTCStatusLogReadOnlyInline(admin.TabularInline):
    model = TBTCStatusLog
    extra = 0
    max_num = 0
    readonly_fields = ('unit', 'status', 'date')
    can_delete = False

#######################################


class TBVTManageInline(admin.TabularInline):
    model = TBVTManage
    extra = 0


class TBVTManageReadOnlyInline(admin.TabularInline):
    model = TBVTManage
    extra = 0
    max_num = 0
    readonly_fields = ('document', 'unit', 'quantity')
    can_delete = False


class TBVTDocumentReadOnlyInline(admin.TabularInline):
    model = TBVTDocument
    extra = 0
    max_num = 0
    readonly_fields = ('MaVB', 'name', 'sponsor', 'date_crt', 'status')
    can_delete = False


###################################################################
# Register


@admin.register(Deparment)
class DeparmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_text')
    list_display_links = ['name', 'short_text']
    inlines = [StaffInline]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    # list_filter = ('staff__name', 'project__name')
    list_display = ('id', 'position_text', 'short_text')
    list_display_links = ['position_text', 'short_text']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm
    list_display = ('MaNV', 'name', 'position', 'deparment',
                    'office', 'd_in', 'd_out')
    list_display_links = [
        'MaNV', 'name', 'position', 'deparment', 'd_in', 'd_out']
    list_filter = ('office', 'position', 'deparment')
    list_select_related = ('position', 'deparment')

    search_fields = ['MaNV', 'name']
    list_per_page = 25
    actions_on_bottom = True
    save_on_top = True
    inlines = [AllocationInline]
    fieldsets = (
        ('Thông tin chung', {'fields': (
            ('MaNV'),
            ('name', 'dob'),
            ('position', 'deparment', 'office'),
            ('pros', 'certi'),
            ('d_in', 'd_out'),
            )}),
        ('Thông tin cá nhân', {
            'fields': ('cmnd', 'pob', 'hk', 'address', 'tel'),
            'classes': ('collapse')
            })
        )

    readonly_fields = ["MaNV"]

    class Media:
        css = {"all": ("css/forms.css",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('location', 'status')
    list_display = ('id', 'name', 'location', 'status')
    list_display_links = ('name', 'location', 'status')

    inlines = [AllocationInline,
               TBTCDocumentReadOnlyInline, TBVTDocumentReadOnlyInline]
    filter_horizontal = ('allowed_users',)
    fields = ('name', 'location', 'description', 'chief',
              ('status', 'no_paid'),  'note', 'allowed_users')


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_filter = ('staff', 'project')
    list_display = ('id', 'staff', 'deparment', 'position',
                    'project', 'd_in', 'd_out')
    list_display_links = ('staff', 'deparment', 'position', 'project')
    list_select_related = ('staff', 'project')

    def deparment(self, obj):
        return str(obj.staff.deparment)
    deparment.short_description = 'Bộ phận'

    def position(self, obj):
        return str(obj.staff.position)
    position.short_description = 'Chức vụ'


@admin.register(DateLog)
class DateLogAdmin(admin.ModelAdmin):
    list_filter = ('staff__name', 'project', 'date')
    list_display = ('id', 'date', 'staff', 'project',
                    'shift1', 'shift2', 'shift3', 'over9')
    list_display_links = ('staff', 'project')
    list_select_related = ('staff', 'project')

#######################################


@admin.register(TBTC)
class TBTCAdmin(admin.ModelAdmin):
    form = TBTCAdminForm

    list_display = ('MaTBTC', 'type', 'brand',
                    'project', 'sponsor', 'd_in', 'd_out')
    list_display_links = ['MaTBTC', 'type', 'brand',
                          'project', 'sponsor', 'd_in', 'd_out']
    list_filter = ('type', 'brand')
    list_select_related = ('type', 'brand')
    list_per_page = 25
    search_fields = ['MaTBTC', 'type', 'brand']
    actions_on_bottom = True
    save_on_top = True
    fields = ('MaTBTC', 'type', 'brand', 'd_in', 'd_out')
    readonly_fields = ["MaTBTC"]

    inlines = [TBTCManageInline, TBTCStatusLogReadOnlyInline]

    class Media:
        css = {"all": ("css/forms.css",)}

    def project(self, obj):
        current = TBTCManage.objects.filter(
            unit=obj, d_return__isnull=True).latest('d_receive')
        return str(current.d_receive.project)
    project.short_description = 'Công trình'

    def sponsor(self, obj):
        current = TBTCManage.objects.filter(
            unit=obj, d_return__isnull=True).latest('d_receive')
        return str(current.d_receive.sponsor)
    sponsor.short_description = 'Quản lý'


@admin.register(TBTCDocument)
class TBTCDocumentAdmin(admin.ModelAdmin):
    list_display = ('MaVB', 'name', 'project', 'sponsor', 'date_crt')
    list_display_links = ['MaVB', 'name', 'project', 'sponsor', 'date_crt']
    list_filter = ('MaVB', 'name', 'project', 'sponsor')
    search_fields = ['MaNV', 'name', 'project', 'sponsor']
    inlines = [TBTCReceiveInline, TBTCReturnInline]


@admin.register(TBTCManage)
class TBTCManageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'unit', 'project', 'sponsor', 'd_receive', 'd_return'
        )
    list_display_links = (
        'id', 'unit', 'project', 'sponsor', 'd_receive', 'd_return'
        )
    list_select_related = ('unit', 'd_receive', 'd_return')

    def project(self, obj):
        return str(obj.d_receive.project)
    project.short_description = 'Công trình'

    def sponsor(self, obj):
        return str(obj.d_receive.sponsor)
    sponsor.short_description = 'Quản lý'


@admin.register(TBTCStatusLog)
class TBTCStatusLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'status', 'date')
    list_display_links = ['unit', 'status', 'date']


@admin.register(TBTCType)
class TBTCTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_text')
    list_display_links = ['name', 'short_text']


@admin.register(TBTCBrand)
class TBTCBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_text')
    list_display_links = ['name', 'short_text']

#######################################


@admin.register(TBVTDocument)
class TBVTDocumentAdmin(admin.ModelAdmin):
    list_display = ('MaVB', 'name', 'project', 'sponsor', 'date_crt')
    list_display_links = ['MaVB', 'name', 'project', 'sponsor', 'date_crt']
    inlines = [TBVTManageInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('status',)
        return self.readonly_fields


@admin.register(TBVT)
class TBVTAdmin(admin.ModelAdmin):
    list_display = ('MaTBVT', 'type', 'brand', 'unit_m', 'quantity')
    list_display_links = ['MaTBVT', 'type', 'brand', 'unit_m', 'quantity']
    list_filter = ('type', 'brand')
    list_select_related = ('type', 'brand', 'unit_m')
    list_per_page = 25
    search_fields = ['MaTBTC', 'type', 'brand']
    actions_on_bottom = True
    save_on_top = True
    fields = ('MaTBVT', 'type', 'brand', ('quantity', 'unit_m'))
    readonly_fields = ["MaTBVT"]
    inlines = [TBVTManageReadOnlyInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['quantity']
        return self.readonly_fields

    class Media:
        css = {"all": ("css/forms.css",)}


@admin.register(TBVTManage)
class TBVTManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'unit', 'quantity')
    list_display_links = ['document', 'unit', 'quantity']


@admin.register(TBVTType)
class TBVTTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_text')
    list_display_links = ['name', 'short_text']


@admin.register(TBVTBrand)
class TBVTBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_text')
    list_display_links = ['name', 'short_text']


@admin.register(UnitMeasure)
class UnitMeasureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ['name']
