from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, PermissionHelper, modeladmin_register)
from .models import Activities
from crum import get_current_user


class ActivitiesAdmin(ModelAdmin):
    model = Activities
    #button_helper_class = ControllerButtonHelper   # Uncomment this to enable button
    #inspect_view_enabled = True
    menu_label = 'Activity'  # ditch this to use verbose_name_plural from model
    menu_icon = 'cog'  # change as required
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

    def get_queryset(self, request):
        #current_user = get_user()
        current_user = get_current_user()
        if not current_user.is_superuser:
            if current_user.clinic.is_no_org:
                return Activities.objects.filter(user=current_user)
            else:
                return Activities.objects.filter(clinic=current_user.clinic)
        else:
            return Activities.objects.all()


modeladmin_register(ActivitiesAdmin)
