from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, PermissionHelper, EditView, ButtonHelper)
from .models import Schedules
from crum import get_current_user


class SchedulesPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        if user.is_superuser:
            return False
        else:
            return True

    def user_can_delete_obj(self, user, obj):
        if obj.is_done:
            return False
        else:
            return True

    def user_can_edit_obj(self, user, obj):
        if user.is_superuser:
            return False
        else:
            return True
            '''
            if obj.is_done:
                return False
            else:
                return True
            '''


class SchedulesEditView(EditView):
    def get_success_url(self):
        return self.edit_url

    def get_page_title(self):
        return '{} - {}'.format(self.instance.student.name, self.instance.therapist.name)

    def get_page_subtitle(self):
        return '({})'.format(self.instance.activity)


class SchedulesAdmin(ModelAdmin):
    model = Schedules
    base_url_path = 'schedule'  # customise the URL from default to admin/bookadmin
    menu_label = 'Jadwal'  # ditch this to use verbose_name_plural from model
    menu_icon = 'date'  # change as required
    menu_order = 100  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ['date', 'start', 'end', 'student', 'therapist', 'activity',
                    'session', 'is_done', 'additional_info']
    search_fields = ['date', 'student__name', 'therapist__name', 'activity__name']
    list_filter = ['date', 'therapist__name', 'is_done']
    ordering = ['-date', 'start']
    list_export = ['date', 'start', 'end', 'student', 'therapist', 'activity', 'is_done']
    edit_view_class = SchedulesEditView
    permission_helper_class = SchedulesPermissionHelper
    form_view_extra_js = ['schedule/js/schedule.js']
    #inspect_view_enabled = True

    def get_queryset(self, request):
        #current_user = get_user()
        current_user = get_current_user()
        if not current_user.is_superuser:
            if current_user.clinic.is_no_org:
                return Schedules.objects.filter(user=current_user)
            else:
                return Schedules.objects.filter(clinic=current_user.clinic)
        else:
            return Schedules.objects.all()


modeladmin_register(SchedulesAdmin)

