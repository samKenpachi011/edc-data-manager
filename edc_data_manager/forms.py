from django import forms

from .models import DataActionItem


class DataActionItemForm(forms.ModelForm):

    class Meta:
        model = DataActionItem
        fields = '__all__'
