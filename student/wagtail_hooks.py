from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, PermissionHelper, EditView, ButtonHelper)
from .models import Students
from crum import get_current_user


class StudentsEditView(EditView):
    def get_success_url(self):
        return self.edit_url


class StudentsAdmin(ModelAdmin):
    model = Students
    base_url_path = 'student'  # customise the URL from default to admin/bookadmin
    menu_label = 'Siswa'  # ditch this to use verbose_name_plural from model
    menu_icon = 'user'  # change as required
    menu_order = 70  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ['name', 'dob', 'calculate_age', 'address']
    search_fields = ('name', 'dob', )
    edit_view_class = StudentsEditView

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
