from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, PermissionHelper, EditView, ButtonHelper)
from .models import Therapists
from crum import get_current_user


class TherapistsEditView(EditView):
    def get_success_url(self):
        return self.edit_url


class TherapistsAdmin(ModelAdmin):
    model = Therapists
    base_url_path = 'therapist'  # customise the URL from default to admin/bookadmin
    menu_label = 'Therapist'  # ditch this to use verbose_name_plural from model
    menu_icon = 'group'  # change as required
    menu_order = 80  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ['name', 'mobile', 'address', 'education']
    search_fields = ('name', 'mobile',)
    edit_view_class = TherapistsEditView

    def get_queryset(self, request):
        #current_user = get_user()
        current_user = get_current_user()
        if not current_user.is_superuser:
            if current_user.clinic.is_no_org:
                return Therapists.objects.filter(user=current_user)
            else:
                return Therapists.objects.filter(clinic=current_user.clinic)
        else:
            return Therapists.objects.all()


modeladmin_register(TherapistsAdmin)
