from django import forms

from .models import DataActionItem


class DataActionItemForm(forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super(DataActionItemForm, self).__init__(*args, **kwargs)
        self.fields['assigned'].widget = forms.RadioSelect(
            choices=self.instance.assign_users)

    class Meta:
        model = DataActionItem
        fields = '__all__'
