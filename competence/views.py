from django.shortcuts import render
from datetime import datetime as dt
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import user_passes_test

from .models import AnswerDetail, AbilityTest, FormVersion
# , QADetail AbilityType, QuestionDetail
from summary.models import Staff  # , Allocation, Project


@never_cache
@user_passes_test(lambda u: u.has_perm('competence.abi_test'))
def staffs_tests(request):
    render_content = {}
    if "POST" == request.method:
        post_input = request.POST.dict()
        if 'None' in post_input.values():
            render_content.update({
                'err_mess': 'Vui lòng điền đầy đủ thông tin'})
        else:
            qs = '-'.join(k[5:] for k in post_input.keys() if 'form=' in k)
            form = FormVersion.objects.get(construct=qs)
            staff = Staff.objects.get(name=post_input['next-staff'])
            sponsor = Staff.objects.get(name=post_input['next-sponsor'])
            date = dt.strptime(post_input['next-date'], '%Y-%m-%d').date()
            test = AbilityTest.objects.filter(
                form_version=form, staff=staff, sponsor=sponsor, date=date)
            if test.exists() is not True:
                test = AbilityTest.objects.create(
                    form_version=form, staff=staff, sponsor=sponsor, date=date)
                for qa in test.qadetail_set.all():
                    answer = AnswerDetail.objects.get(
                        question__code=qa.question.code,
                        rank=post_input['form=' + str(qa.question.code)])
                    qa.answer = answer
                    qa.save()
            else:
                render_content.update({
                    'err_mess': 'Đánh giá này đã được lưu lại trước đây, \
                    vui lòng kiểm tra lại '})
    else:
        pass

    staffs_tests = dict()
    staff_list = Staff.objects.filter(d_out__isnull=True)
    # version_count = \
    #    AbilityTest.objects.order_by('version').distinct('version').count()
    # for ver in range(version_count):
    if AbilityTest.objects.all().exists():
        tests_info = AbilityTest.objects.first().qadetail_set.all()
        render_content.update({'tests_info': tests_info})

    for staff in staff_list:
        staff_tests = AbilityTest.objects.filter(staff=staff)
        if staff_tests.exists():
            staffs_tests[staff] = [test for test in staff_tests]

    render_content.update({
        'staffs_tests': staffs_tests, 'staff_list': staff_list})

    return render(request, 'competence/staffs.html', render_content)
