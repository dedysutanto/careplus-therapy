from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, PermissionHelper, modeladmin_register)
from .models import Clinic, User
from crum import get_current_user


class ClinicAdmin(ModelAdmin):
    model = Clinic
    #button_helper_class = ControllerButtonHelper   # Uncomment this to enable button
    #inspect_view_enabled = True
    menu_label = 'Klinik'  # ditch this to use verbose_name_plural from model
    menu_icon = 'group'  # change as required
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'start', 'end')
    search_fields = ('name',)

    def get_queryset(self, request):
        #current_user = get_user()
        current_user = get_current_user()
        if not current_user.is_superuser:
            if current_user.clinic.is_no_org:
                return Clinic.objects.all()
            else:
                return Clinic.objects.filter(id=current_user.clinic.id)
        else:
            return Clinic.objects.all()


modeladmin_register(ClinicAdmin)
