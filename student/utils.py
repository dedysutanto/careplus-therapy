from invoice.models import Invoices, InvoiceItems
from schedule.models import Schedules
from student.models import Students
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist


def update_student_session(sender, instance, created):
    all_student_invoices = Invoices.objects.filter(student=instance.student)
    print('all_student_inovices', all_student_invoices)
    total_invoice_session = 0
    for invoice in all_student_invoices:
        invoice_items = InvoiceItems.objects.filter(invoice=invoice)
        sub_invoice_session = 0
        for invoice_item in invoice_items:
            print(invoice_item.item.session)
            sub_invoice_session += invoice_item.item.session
        print('sub_invoice_session', sub_invoice_session)
        total_invoice_session += sub_invoice_session
        print('total_invoice_session', total_invoice_session)

    sub_schedule_session = Schedules.objects.filter(student=instance.student, is_done=True).aggregate(Sum('session'))
    sub_schedule_session_not_done = Schedules.objects.filter(
        student=instance.student, is_done=False
    ).aggregate(Sum('session'))

    total_session = total_invoice_session
    total_schedule_session = 0
    if sub_schedule_session['session__sum']:
        print('sub_schedule_session', sub_schedule_session)
        total_schedule_session = sub_schedule_session['session__sum']
        print('total_schedule_session', total_schedule_session)
        total_session = total_invoice_session - total_schedule_session

    total_schedule_session_not_done = 0
    if sub_schedule_session_not_done['session__sum']:
        print('sub_schedule_session_not_done', sub_schedule_session_not_done)
        total_schedule_session_not_done = sub_schedule_session_not_done['session__sum']
        print('total_schedule_session_not_done', total_schedule_session_not_done)
        total_session -= total_schedule_session_not_done

    if total_session > 0:
        try:
            student = Students.objects.get(id=instance.student.id)
            student.session = total_session
            student.session_used = total_schedule_session
            student.session_scheduled = total_schedule_session_not_done
            print('Student Session', student.session)
            student.save()

        except ObjectDoesNotExist:
            pass