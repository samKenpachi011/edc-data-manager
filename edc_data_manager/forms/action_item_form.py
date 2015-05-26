from django import forms
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from ..models import ActionItem


def group_choices():
    group_choices = []
    for item in Group.objects.values('name').all():
        group_choices.append(item.get('name'), ' '.join(item.get('name').split('_')))
    return group_choices


class ActionItemForm(forms.ModelForm):

    action_group = forms.ChoiceField(
        label='Action group',
        choices=group_choices(),
        help_text=('You can only select a group to which you belong. '
                   'Choices are based on Groups defined in Auth.'),
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    class Meta:
        model = ActionItem
