from django import forms

from .models import ActionItem


class ActionItemForm(forms.ModelForm):

    class Meta:
        model = ActionItem
        fields = '__all__'
