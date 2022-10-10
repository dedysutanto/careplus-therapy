from django.db import models
from therapist.models import Therapists
from student.models import Students
from account.models import User, Clinic
from data_support.models import Activities
from django.utils.translation import gettext_lazy as _
from crum import get_current_user
from datetime import timedelta, time
from wagtail.admin.panels import FieldPanel, InlinePanel, \
    FieldRowPanel, MultiFieldPanel, HelpPanel, TabbedInterface


SESSION = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
]


class Schedules(models.Model):
    def limit_choices_to_current_user():
        user = get_current_user()
        if not user.is_superuser:
            return {'user': user}
        else:
            return {}

    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField(blank=True, null=True)
    session = models.IntegerField(choices=SESSION, default=1)
    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        verbose_name='Siswa',
        limit_choices_to=limit_choices_to_current_user,
    )
    therapist = models.ForeignKey(
        Therapists,
        on_delete=models.CASCADE,
        verbose_name='Therapist',
        limit_choices_to=limit_choices_to_current_user,
    )

    activity = models.ForeignKey(
        Activities,
        on_delete=models.CASCADE,
        verbose_name='Activity',
        limit_choices_to=limit_choices_to_current_user,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_('Owner'),
        null=True
    )

    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.SET_NULL,
        verbose_name=_('Klinik'),
        null=True
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([FieldPanel('date'), FieldPanel('start'), FieldPanel('session')]),
            FieldPanel('student'),
            FieldPanel('therapist'),
            FieldPanel('activity')
        ], heading='Setup Schedule', classname='')
    ]

    class Meta:
        db_table = 'schedule'
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'

    def __str__(self):
        return '%s' % self.start

    def save(self):
        if self.user is None:
            current_user = get_current_user()
            self.user = current_user
            self.clinic = current_user.clinic

        #self.end = self.start.hour + timedelta(hours=self.session)
        print(self.start.hour)
        print(self.session)
        #self.end = self.start
        self.end = time(hour=self.start.hour + self.session, minute=self.start.minute)

        return super(Schedules, self).save()

