from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from invoice.models import Invoices
from schedule.models import Schedules
from .utils import update_student_session


@receiver(post_save, sender=Invoices)
def update_student_session_from_invoice(sender, instance, created, **kwargs):
    if created:
        print('Update Student Session from Invoice Created')
        transaction.on_commit(lambda: update_student_session(sender, instance, created))
        update_student_session(sender, instance, created)
    else:
        transaction.on_commit(lambda: update_student_session(sender, instance, created))
        #update_student_session(sender, instance, created)
        print('Update Student Session from Invoice Updated')


@receiver(post_save, sender=Schedules)
def update_student_session_from_schedule(sender, instance, created, **kwargs):
    transaction.on_commit(lambda: update_student_session(sender, instance, created))
    #update_student_session(sender, instance, created)
    print('Update Student Session from Schedule')


@receiver(post_delete, sender=Invoices)
def update_student_session_from_invoice_delete(sender, instance, using, **kwargs):
    transaction.on_commit(lambda: update_student_session(sender, instance, using))
    print('Update Student Session from Invoice Delete')


@receiver(post_delete, sender=Schedules)
def update_student_session_from_schedule_delete(sender, instance, using, **kwargs):
    transaction.on_commit(lambda: update_student_session(sender, instance, using))
    #update_student_session(sender, instance, using)
    print('Update Student Session from Schedule Delete')
