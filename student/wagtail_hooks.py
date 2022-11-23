from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, PermissionHelper, EditView, ButtonHelper)
from .models import Students
from crum import get_current_user


class StudentPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        if user.is_superuser:
            return False
        else:
            return True

    def user_can_delete_obj(self, user, obj):
        if user.is_superuser:
            return False
        else:
            return False

    def user_can_edit_obj(self, user, obj):
        if user.is_superuser:
            return False
        else:
            return True


class StudentsEditView(EditView):
    def get_success_url(self):
        return self.edit_url

    def get_page_title(self):
        return self.instance.name

    def get_page_subtitle(self):
        return '({} sesi)'.format(self.instance.session)


class StudentsAdmin(ModelAdmin):
    model = Students
    base_url_path = 'student'  # customise the URL from default to admin/bookadmin
    menu_label = 'Siswa'  # ditch this to use verbose_name_plural from model
    menu_icon = 'user'  # change as required
    menu_order = 70  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ['name', 'dob', 'calculate_age', 'session', 'session_used', 'session_scheduled',
                    'address', 'additional_info',]
    search_fields = ('name', 'dob', )
    edit_view_class = StudentsEditView
    permission_helper_class = StudentPermissionHelper
    inspect_view_enabled = True

    def get_queryset(self, request):
        #current_user = get_user()
        current_user = get_current_user()
        if not current_user.is_superuser:
            if current_user.clinic.is_no_org:
                return Students.objects.filter(user=current_user)
            else:
                return Students.objects.filter(clinic=current_user.clinic)
        else:
            return Students.objects.all()


modeladmin_register(StudentsAdmin)
