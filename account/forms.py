from django import forms
from wagtail.users.forms import UserEditForm, UserCreationForm
from .models import User, Clinic
from django.utils.translation import gettext_lazy as _


class CustomUserEditForm(UserEditForm):
    clinic = forms.ModelChoiceField(queryset=Clinic.objects,
                                    required=True,
                                    disabled=False,
                                    label=_('Klinik'))


class CustomUserCreationForm(UserCreationForm):
    clinic = forms.ModelChoiceField(queryset=Clinic.objects,
                                    required=True,
                                    label=_('Klinik'))
