from wagtail.admin.ui.components import Component
from student.models import Students
from therapist.models import Therapists
from schedule.models import Schedules
from invoice.models import InvoiceItems, Invoices
from crum import get_current_user
from random import randint
from django.utils.translation import gettext as _
from django.utils.timezone import now, timedelta


class SummaryPanel(Component):
    order = 50
    template_name = "dashboard/site_summary.html"

    def __init__(self):
        today = now()
        prev_month = today.replace(day=1) - timedelta(days=1)
        self.period_start = prev_month.replace(day=26, hour=0)
        self.period_end = today.replace(day=25, hour=0)
        # print(self.period_start)
        # print(self.period_end)

        user = get_current_user()
        if user.is_superuser:
            self.students = Students.objects.all().count()
            self.therapists = Therapists.objects.all().count()
            self.session_done = Schedules.objects.filter(
                is_done=True,
                date__range=[self.period_start, self.period_end]
            ).count()
            self.session_scheduled = Schedules.objects.filter(
                is_done=False,
                date__range=[self.period_start, self.period_end]
            ).count()
            self.invoice_paid = Invoices.objects.filter(
                is_paid=True,
                datetime__range=[self.period_start, self.period_end]
            ).count()
            self.invoice_unpaid = Invoices.objects.filter(
                is_paid=False,
                datetime__range=[self.period_start, self.period_end]
            ).count()
        elif user.clinic:
            self.students = Students.objects.filter(clinic=user.clinic).count()
            self.therapists = Therapists.objects.filter(clinic=user.clinic).count()
            self.session_done = Schedules.objects.filter(
                clinic=user.clinic,
                is_done=True,
                date__range=[self.period_start, self.period_end]
            ).count()
            self.session_scheduled = Schedules.objects.filter(
                clinic=user.clinic,
                is_done=False,
                date__range = [self.period_start, self.period_end]
            ).count()
            self.invoice_paid = Invoices.objects.filter(
                clinic=user.clinic,
                is_paid=True,
                datetime__range=[self.period_start, self.period_end]
            ).count()
            self.invoice_unpaid = Invoices.objects.filter(
                clinic=user.clinic,
                is_paid=False,
                datetime__range=[self.period_start, self.period_end]
            ).count()

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['students'] = self.students
        context['therapists'] = self.therapists
        context['session_done'] = self.session_done
        context['session_scheduled'] = self.session_scheduled
        context['period_start'] = self.period_start
        context['period_end'] = self.period_end
        context['invoice_paid'] = self.invoice_paid
        context['invoice_unpaid'] = self.invoice_unpaid

        return context


class ScheduleTodayPanel(Component):
    order = 60
    template_name = 'dashboard/schedule_today.html'

    def __init__(self):
        user = get_current_user()
        self.today = now()
        if user.is_superuser:
            self.schedule_today = Schedules.objects.filter(date=self.today)
        elif user.clinic:
            self.schedule_today = Schedules.objects.filter(
                clinic=user.clinic, date=self.today)

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        panel_title = 'Jadwal Hari Ini'

        context['panel_title'] = panel_title
        context['schedule_today'] = self.schedule_today
        context['today'] = self.today

        return context


class MemberChartsPanel(Component):
    order = 70
    template_name = 'dashboard/members_charts.html'

    def __init__(self):
        user = get_current_user()
        self.member_status = {
            'DIRECT': 0,
            'RELAY': 0,
            'OFFLINE': 0
        }
        self.member_version = {}
        if user.is_superuser:
            members = Members.objects.all()
        elif user.organization.is_no_org:
            members = Members.objects.filter(user=user)
        else:
            members = Members.objects.filter(organization=user.organization)

        for member in members:
            peers = to_dictionary(member.peers.peers)

            if 'paths' in peers and len(peers['paths']) != 0:
                version = str(peers['version'])
                latency = peers['latency']
                try:
                    self.member_version['v' + version]
                    self.member_version['v' + version] += 1
                except KeyError:
                    self.member_version['v' + version] = 1

                if latency < 0:
                    self.member_status['RELAY'] += 1
                else:
                    self.member_status['DIRECT'] += 1

            else:
                self.member_status['OFFLINE'] += 1

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        data_status = []
        data_version = []
        labels = ['DIRECT', 'RELAY', 'OFFLINE']
        backgroundColor_status = [
            'rgba(46, 125, 50, 0.7)',
            'rgba(21, 101, 192, 0.7)',
            'rgba(198, 40, 40, 0.7)'
        ]
        backgroundColor_version = []

        labels_version = []

        for member in self.member_status.values():
            data_status.append(member)

        for version in self.member_version:
            labels_version.append(version)
            data_version.append(self.member_version[version])
            backgroundColor_version.append('rgba({}, {}, {}, 0.7'.format(
                randint(0, 100), 125, randint(100, 255)))

        is_data_status = False
        is_data_version = False
        if len(data_version) > 0:
            is_data_version = True

        for data in data_version:
            if data > 0:
                is_data_status = True
                break

        context['labels'] = labels
        context['labels_version'] = labels_version
        context['backgroundColor_status'] = backgroundColor_status
        context['backgroundColor_version'] = backgroundColor_version
        context['data_status'] = data_status
        context['data_version'] = data_version
        context['chart_title_status'] = 'Members Status Distribution'
        context['chart_title_version'] = 'Members Version Distribution'
        context['is_data_status'] = is_data_status
        context['is_data_version'] = is_data_version

        return context
