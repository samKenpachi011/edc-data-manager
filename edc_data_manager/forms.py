from django import forms

from .models import DataActionItem


class DataActionItemForm(forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = DataActionItem
        fields = '__all__'
