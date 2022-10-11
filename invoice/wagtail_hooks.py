from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, PermissionHelper, EditView, ButtonHelper)
from .models import Invoices
from crum import get_current_user


class InvoicesEditView(EditView):
    def get_success_url(self):
        return self.edit_url

    def get_page_title(self):
        return self.instance.student.name

    def get_page_subtitle(self):
        return self.instance.calculate_total


class InvoicesAdmin(ModelAdmin):
    model = Invoices
    base_url_path = 'invoices'  # customise the URL from default to admin/bookadmin
    menu_label = 'Invoice'  # ditch this to use verbose_name_plural from model
    menu_icon = 'success'  # change as required
    menu_order = 90  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = ['datetime', 'student', 'calculate_total', 'is_paid']
    search_fields = ('student__name',)
    list_filter = ['datetime']
    edit_view_class = InvoicesEditView

    def get_queryset(self, request):
        #current_user = get_user()
        current_user = get_current_user()
        if not current_user.is_superuser:
            if current_user.clinic.is_no_org:
                return Invoices.objects.filter(user=current_user)
            else:
                return Invoices.objects.filter(clinic=current_user.clinic)
        else:
            return Invoices.objects.all()


modeladmin_register(InvoicesAdmin)
