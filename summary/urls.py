from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('index/', views.index, name='index'),
    path('', RedirectView.as_view(url='sites/')),

    path('sites/', views.site_list, name='site_list'),
    path('staffs/', views.staff_list, name='staff_list'),
    path('staffs/history', views.staffs_history, name='staffs_history'),
    path('staff/<int:staff_id>', views.staff_detail, name='staff_detail'),

    path('project/<int:project_id>',
         views.project_detail, name='project_detail'),
    path('project/<int:project_id>/monthreport',
         views.p_m_report, name='p_m_report'),
    path('project/<int:project_id>/check',
         views.project_check, name='project_check'),

    path('office/', views.office_detail, name='office_detail'),
    path('office/check', views.office_check, name='office_check'),
    path('office/monthreport', views.o_m_report, name='o_m_report'),

    url('export_mreport_excel',
        views.export_mreport_excel, name='export_mreport_excel'),
    url('export_tbtc_excel',
        views.export_tbtc_excel, name='export_tbtc_excel'),

    path('TBTC/', views.tbtc_list, name='tbtc_list'),
    path('TBTC/<int:TBTC_id>',
         views.tbtc_manage, name='tbtc_manage'),

    path('TBVT/', views.tbvt_list, name='tbvt_list'),

    path('datelog_full/', views.datelog_full, name='datelog_full'),
]
