# from random import randint
# from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist
from wagtail.admin.ui.components import Component
from crum import get_current_user
from django.utils.timezone import now, timedelta
from schedule.wagtail_hooks import SchedulesAdmin
from therapist.models import Therapists
from schedule.models import Schedules
from student.models import Students
from invoice.models import Invoices
from data_support.models import Activities


def get_current_period():
    today = now()
    print('Date', today.day)
    if today.day > 25:
        prev_month = today
        next_month = today.replace(day=1) + timedelta(days=32)   
    else:
        prev_month = today.replace(day=1) - timedelta(days=1)
        next_month = today
    period_start = prev_month.replace(day=26, hour=0)
    period_end = next_month.replace(day=25, hour=0)

    return period_start, period_end


class ListPeriodePanel(Component):
    order = 40
    template_name = "dashboard/list_periode.html"
    
    def __init__(self):
        pass


class SummaryPanel(Component):
    order = 50
    template_name = "dashboard/site_summary.html"

    def __init__(self):
        self.period_start, self.period_end = get_current_period()

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
        self.url_helper = SchedulesAdmin().url_helper
        if user.is_superuser:
            self.schedule_today = Schedules.objects.filter(date=self.today)
        elif user.clinic:
            self.schedule_today = Schedules.objects.filter(
                clinic=user.clinic, date=self.today)

        if self.schedule_today:
            for schedule in self.schedule_today:
                schedule.edit_url = self.url_helper.get_action_url('edit', schedule.id)

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        panel_title = 'Jadwal Hari Ini'

        context['panel_title'] = panel_title
        context['schedule_today'] = self.schedule_today
        context['today'] = self.today
        context['create_url'] = self.url_helper.get_action_url('create')

        return context


class SummaryTherapist(Component):
    order = 55
    template_name = 'dashboard/summary_therapist.html'

    def __init__(self):
        user = get_current_user()
        self.period_start, self.period_end = get_current_period()
        if user.is_superuser:
            self.therapists = Therapists.objects.all()
        elif user.clinic:
            self.therapists = Therapists.objects.filter(clinic=user.clinic)

        try:
            observation = Activities.objects.get(name__icontains='obser')
            print(observation)
        except ObjectDoesNotExist:
            observation = None
            
        self.therapists_summary = []
        for therapist in self.therapists:
            print(therapist)
            schedule_ob = Schedules.objects.filter(
                date__range=[self.period_start, self.period_end],
                therapist=therapist,
                is_done=True,
                activity=observation
            )
            if schedule_ob:
                therapist.session_ob = schedule_ob.count()
            else:
                therapist.session_ob = 0

            schedule_th = Schedules.objects.filter(
                date__range=[self.period_start, self.period_end],
                therapist=therapist,
                is_done=True
            ).exclude(
                activity=observation
            )
            if schedule_th:
                therapist.session_not_ob_done = schedule_th.count()
            else:
                therapist.session_not_ob_done = 0

            schedule_th_undone = Schedules.objects.filter(
                date__range=[self.period_start, self.period_end],
                therapist=therapist,
                is_done=False
            ).exclude(
                activity=observation
            )
            if schedule_th_undone:
                therapist.session_not_ob_undone = schedule_th_undone.count()
            else:
                therapist.session_not_ob_undone = 0

            self.therapists_summary.append(therapist)

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        panel_title = 'Summary Therapist'

        context['panel_title'] = panel_title
        context['therapists'] = self.therapists_summary
        context['period_start'] = self.period_start
        context['period_end'] = self.period_end

        return context


'''
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
                    # self.member_version['v' + version]
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
'''
