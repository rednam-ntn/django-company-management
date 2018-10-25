from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .models import TBVTManage  # TBVTDocument


# update number of TBVT in storage after import and export
@receiver(pre_save, sender=TBVTManage)
def TBVTManage_change_update(sender, instance, **kwargs):
    if instance.id:
        old = TBVTManage.objects.get(pk=instance.id)
        if old.document.status == 'im':
            if instance.document.status == 'im':
                instance.unit.quantity = \
                    instance.unit.quantity - old.quantity + instance.quantity
        elif old.document.status == 'ex':
            if instance.document.status == 'ex':
                instance.unit.quantity =\
                    instance.unit.quantity + old.quantity - instance.quantity
    else:
        if instance.document.status == 'im':
            instance.unit.quantity += instance.quantity
        elif instance.document.status == 'ex':
            instance.unit.quantity -= instance.quantity

    instance.unit.save()


@receiver(pre_delete, sender=TBVTManage)
def TBVTManage_delete_update(sender, instance, **kwargs):
    if instance.document.status == 'im':
        instance.unit.quantity -= instance.quantity
    elif instance.document.status == 'ex':
        instance.unit.quantity += instance.quantity

    instance.unit.save()
