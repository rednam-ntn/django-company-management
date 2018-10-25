from django.db.models.signals import pre_save, post_save  # , pre_delete
from django.dispatch import receiver

from .models import QADetail, AbilityTest, QuestionDetail


# update result of AbilityTest in db when create QADetail
@receiver(pre_save, sender=QADetail)
def test_result_update(sender, instance, **kwargs):
    test = instance.test
    qa_list = QADetail.objects.filter(test=test)
    if qa_list.exists():
        rank = dict()
        for qa in qa_list:
            if qa.answer:
                if qa.question.code in str(test.form_version):
                    rank[qa.answer.rank] = rank.get(qa.answer.rank, 0) + 1
        if len(rank) > 2:
            rank_list = sorted(([c, r] for r, c in rank.items()), reverse=True)
            asc_list = sorted(([r, c] for r, c in rank.items()), reverse=True)
            if len(rank_list) < 3:
                top_rank = rank_list[0][1]
                if top_rank - rank_list[1][1] > 2:
                    top_rank = rank_list[1][1] + 1
            else:
                count = 0
                top_rank = 0
                for c, r in asc_list:
                    count += c
                    if count >= 8:
                        if r - asc_list[-1][0] < 2:
                            top_rank = r
                            break
                        else:
                            top_rank = asc_list[-1][0] + 1
                            break

            test.result = top_rank
            test.save()
    else:
        if instance.answer:
            test.result = instance.answer.rank
            test.save()


# Create QADetail when create or update AbilityTest
@receiver(post_save, sender=AbilityTest)
def create_test_qa(sender, instance, **kwargs):
    qa_list = QADetail.objects.filter(test=instance)
    if qa_list.exists() is not True:
        num_order = 0
        for qa_code in str(instance.form_version).split('-'):
            num_order += 1
            question = QuestionDetail.objects.get(code=qa_code)
            QADetail.objects.create(test=instance, question=question,
                                    num_order=num_order)


# Create QuestionDetail code
@receiver(pre_save, sender=QuestionDetail)
def update_q_code(sender, instance, **kwargs):
    num_order = QuestionDetail.objects.filter(type=instance.type).count() + 1
    instance.code = instance.type.short_text + '_' + str(num_order)
    instance.save()
