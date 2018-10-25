from django.urls import path
# from django.conf.urls import url
from . import views
from django.views.generic import RedirectView


urlpatterns = [
    path('staffs_tests/', views.staffs_tests, name='staffs_tests'),
    path('', RedirectView.as_view(url='staffs/')),
]
