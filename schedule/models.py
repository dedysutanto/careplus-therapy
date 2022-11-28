from datetime import time
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from crum import get_current_user
from wagtail.admin.panels import FieldPanel, \
    FieldRowPanel, MultiFieldPanel
from django.core.exceptions import ValidationError
from django.db import models
from therapist.models import Therapists
from student.models import Students
from account.models import User, Clinic
from data_support.models import Activities


SESSION = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
]


class Schedules(models.Model):
    def limit_choices_to_current_user():
        user = get_current_user()
        if not user.is_superuser:
            return {'user': user}
        else:
            return {}

    date = models.DateField('Tanggal')
    start = models.TimeField('Mulai')
    end = models.TimeField('Selesai', blank=True, null=True)
    session = models.IntegerField('Sesi', choices=SESSION, default=1)
    additional_info = models.TextField('Keterangan', blank=True, null=True)
    is_done = models.BooleanField('Terapi Selesai', default=False)
    is_arrived = models.BooleanField('Sudah Hadir', default=False)

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
            FieldPanel('activity'),
            FieldPanel('additional_info'),
            FieldRowPanel([FieldPanel('is_arrived'), FieldPanel('is_done')])
        ], heading='Setup Schedule', classname='')
    ]

    class Meta:
        db_table = 'schedule'
        verbose_name = 'Jadwal'
        verbose_name_plural = 'Jadwal'

    def __str__(self):
        return '%s' % self.start

    def clean(self):
        if self.user is None:
            current_user = get_current_user()
            self.user = current_user
            self.clinic = current_user.clinic

        '''
        This is to ensure that Session is updated
        '''

        try:
            self.student
            if self.student:
                from student import utils
                utils.update_student_session(None, self, None)

        except ObjectDoesNotExist:
            raise ValidationError('Siswa: Kolom ini harus diisi.')

        '''
        Check Time Schedule against operational
        DISABLE

        if self.start < self.user.clinic.start or self.start > self.user.clinic.end:
            raise ValidationError('Jam mulai terapi diluar jam operational klinik')

        end = time(hour=self.start.hour + self.session, minute=self.start.minute)

        if end < self.user.clinic.start or end > self.user.clinic.end:
            raise ValidationError('Jam selesai terapi diluar jam operational klinik')
        '''

        '''
        Check if Student still have session
        '''
        self.student = Students.objects.get(id=self.student.id)
        if self.id:
            if (self.student.session + self.session) < self.session and self.id is None:
                raise ValidationError(
                    'Sesi siswa tidak cukup. {} hanya memilik {} sesi tersisa'.format(self.student,
                                                                                      self.student.session)
                )
        else:
            if self.student.session < self.session:
                raise ValidationError(
                    'Sesi siswa tidak cukup. {} hanya memilik {} sesi tersisa'.format(self.student,
                                                                                      self.student.session)
                )
        '''
        Check if the therapist schedules are conflict
        '''
        therapist_schedules = Schedules.objects.filter(therapist=self.therapist, is_done=False)

        end = time(hour=self.start.hour + self.session, minute=self.start.minute)

        is_conflicted = False
        if therapist_schedules:
            for schedule in therapist_schedules:
                if self.id != schedule.id:
                    if self.date == schedule.date:
                        if self.start == schedule.start:
                            is_conflicted = True
                        if schedule.start < self.start < schedule.end:
                            is_conflicted = True
                        if schedule.start < end < schedule.end:
                            is_conflicted = True

            if is_conflicted:
                raise ValidationError('Jadwal therapist {} konflik!'.format(self.therapist))

        '''
        Check if the Student schedules are conflict
        '''
        '''
        student_schedules = Schedules.objects.filter(student=self.student, is_done=False)

        is_conflicted = False
        if student_schedules:
            for schedule in student_schedules:
                if self.id != schedule.id:
                    if self.date == schedule.date:
                        if self.start == schedule.start:
                            is_conflicted = True
                        if schedule.start < self.start < schedule.end:
                            is_conflicted = True
                        if schedule.start < end < schedule.end:
                            is_conflicted = True

            if is_conflicted:
                raise ValidationError('Jadwal siswa {} konflik!'.format(self.student))
        '''

    def save(self):
        if self.user is None:
            current_user = get_current_user()
            self.user = current_user
            self.clinic = current_user.clinic

        #self.end = self.start.hour + timedelta(hours=self.session)
        # print(self.start.hour)
        # print(self.session)
        #self.end = self.start
        self.end = time(hour=self.start.hour + self.session, minute=self.start.minute)
        if self.is_done:
            self.is_arrived = self.is_done

        return super(Schedules, self).save()

