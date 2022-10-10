from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from config.utils import calculate_age
from wagtail.admin.panels import FieldPanel, InlinePanel, \
    FieldRowPanel, MultiFieldPanel, HelpPanel, TabbedInterface
from account.models import User, Clinic
from crum import get_current_user

GENDER = [
    ('M', 'Laki-Laki'),
    ('F', 'Perempuan')
]

RELIGION = [
    ('CHRISTIAN', 'Kristen'),
    ('CATHOLIC', 'Katholik'),
    ('ORTHODOX', 'Orthodox'),
    ('ISLAM', 'Islam'),
    ('HINDU', 'Hindu'),
    ('BUDDHA', 'Budha'),
]

EDUCATION = [
    ('SD', 'SD'),
    ('SMP', 'SMP'),
    ('SMA', 'SMA/SMK'),
    ('S1', 'S1'),
    ('S2', 'S2'),
    ('S3', 'S3'),
]

OCCUPATION = [
    ('TIDAK_BEKERJA', 'Tidak Bekerja'),
    ('PNS', 'PNS/ASN'),
    ('TNI_POLRI', 'TNI/POLRI'),
    ('PEGAWAI_SWASTA', 'Pegawai Swasta'),
    ('WIRAUSAHA', 'Wira Usaha'),
]


class Students(ClusterableModel):
    name = models.CharField(_('Nama Lengkap'), max_length=100)
    call_name = models.CharField(_('Nama Panggilan'), max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=3, verbose_name=_('Jenis Kelamin'), choices=GENDER, default='M')
    dob = models.DateField(verbose_name=_('Tanggal Lahir'))
    pob = models.CharField(_('Tempat Lahir'), max_length=50, blank=True, null=True)
    address = models.TextField(verbose_name=_('Address'), blank=True, null=True)
    #phone = models.CharField(max_length=50, verbose_name=_('Telephone/HP'), blank=True, null=True)
    religion = models.CharField(max_length=50,
                                verbose_name=_('Agama'),
                                choices=RELIGION,
                                default='CHRISTIAN', blank=True, null=True)
    school_name = models.CharField(_('Nama Sekolah'), max_length=100, blank=True, null=True)
    biological_child = models.BooleanField(_('Apakah Anak Kandung'), default=True)

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
            FieldPanel('name'),
            FieldPanel('call_name'),
            FieldRowPanel([FieldPanel('biological_child'), FieldPanel('gender'), FieldPanel('religion')]),
            FieldRowPanel([FieldPanel('pob'), FieldPanel('dob')]),
            FieldPanel('address'),
            FieldPanel('school_name'),
        ], heading='Data Siswa', classname=''),

        TabbedInterface([
            InlinePanel('related_father', heading="Ayah", label="Data Ayah",
                        classname='collapsed',
                        min_num=0, max_num=1),
            InlinePanel('related_mother', heading="Ibu", label="Data Ibu",
                        classname='collapsed',
                        min_num=0, max_num=1),
            InlinePanel('related_sibling', heading="Kakak/Adik", label="Data Kakak/Adik",
                        classname='collapsed',
                        min_num=0, max_num=1),

        ], heading='Latar Belakang Keluarga', classname='collapsed'),
    ]

    class Meta:
        db_table = 'students'
        verbose_name = 'siswa'
        verbose_name_plural = 'siswa'

    def __str__(self):
        return '%s' % self.name

    def calculate_age(self):
        return '%d' % calculate_age(self.dob)

    calculate_age.short_description = _('Umur')

    def save(self):
        if self.user is None:
            current_user = get_current_user()
            self.user = current_user
            self.clinic = current_user.clinic

        return super(Students, self).save()


class ParentFather(Orderable):
    name = models.CharField(_('Nama Ayah'), max_length=100)
    dob = models.DateField(verbose_name=_('Tanggal Lahir'))
    pob = models.CharField(_('Tempat Lahir'), max_length=50, blank=True, null=True)
    education = models.CharField(_('Pendidikan'), choices=EDUCATION, max_length=10, default='S1')
    occupation = models.CharField(_('Pekerjaan'), choices=OCCUPATION, max_length=20, default='PEGAWAI_SWASTA')
    phone = models.CharField(_('Telpon Rumah/Kantor'), max_length=50, blank=True, null=True)
    mobile = models.CharField(_('Nomor HP'), max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50,
                                verbose_name=_('Agama'),
                                choices=RELIGION,
                                default='CHRISTIAN', blank=True, null=True)

    student = ParentalKey(
        'Students',
        on_delete=models.CASCADE,
        related_name='related_father',
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldRowPanel([FieldPanel('pob'), FieldPanel('dob')]),
            FieldRowPanel([FieldPanel('religion'), FieldPanel('education'), FieldPanel('occupation')]),
            FieldPanel('phone'),
            FieldPanel('mobile')
        ], heading='Data Ayah', classname='')
    ]

    class Meta:
        db_table = 'parent_father'
        verbose_name = 'ayah'
        verbose_name_plural = 'ayah'

    def __str__(self):
        return '%s' % self.name

    def calculate_age(self):
        return '%d' % calculate_age(self.dob)

    calculate_age.short_description = _('Umur')


class ParentMother(Orderable):
    name = models.CharField(_('Nama Ibu'), max_length=100)
    dob = models.DateField(verbose_name=_('Tanggal Lahir'))
    pob = models.CharField(_('Tempat Lahir'), max_length=50, blank=True, null=True)
    education = models.CharField(_('Pendidikan Terakhir'), choices=EDUCATION, max_length=10, default='S1')
    occupation = models.CharField(_('Pekerjaan'), choices=OCCUPATION, max_length=20, default='PEGAWAI_SWASTA')
    phone = models.CharField(_('Telpon Rumah/Kantor'), max_length=50, blank=True, null=True)
    mobile = models.CharField(_('Nomor HP'), max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50,
                                verbose_name=_('Agama'),
                                choices=RELIGION,
                                default='CHRISTIAN', blank=True, null=True)

    student = ParentalKey(
        'Students',
        on_delete=models.CASCADE,
        related_name='related_mother',
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldRowPanel([FieldPanel('pob'), FieldPanel('dob')]),
            FieldRowPanel([FieldPanel('religion'), FieldPanel('education'), FieldPanel('occupation')]),
            FieldPanel('phone'),
            FieldPanel('mobile')
        ], heading='Data Ibu', classname='')
    ]

    class Meta:
        db_table = 'parent_mother'
        verbose_name = 'Ibu'
        verbose_name_plural = 'Ibu'

    def __str__(self):
        return '%s' % self.name

    def calculate_age(self):
        return '%d' % calculate_age(self.dob)

    calculate_age.short_description = _('Umur')


class Sibling(Orderable):
    older_sibling_name = models.CharField(_('Nama Kakak'), max_length=200, blank=True, null=True)
    younger_sibling_name = models.CharField(_('Nama Adik'), max_length=200, blank=True, null=True)
    is_normal = models.BooleanField(_('Apakah ada riwayat keterlambatan tumbuh kembang pada kakak/adik '),
                                    default=False)

    student = ParentalKey(
        'Students',
        on_delete=models.CASCADE,
        related_name='related_sibling',
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('older_sibling_name'),
            FieldPanel('younger_sibling_name'),
            FieldPanel('is_normal')
        ], heading='Data Kakak/Adik', classname='')
    ]

    class Meta:
        db_table = 'sibling'
        verbose_name = 'kakak/Adik'
        verbose_name_plural = 'kakak/Adik'

    def __str__(self):
        if self.older_sibling_name:
            return '%s' % self.older_sibling_name
        elif self.younger_sibling_name:
            return '%s' % self.younger_sibling_name
        else:
            return None
