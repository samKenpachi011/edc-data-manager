from django import forms
from django.core.exceptions import ValidationError

from .models import DataActionItem, QueryName


class DataActionItemForm(forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super(DataActionItemForm, self).__init__(*args, **kwargs)
        self.fields['assigned'].widget = forms.RadioSelect(
            choices=self.instance.assign_users)
        self.fields['query_name'].widget = forms.RadioSelect(
            choices=self.instance.query_names)
    
    def clean(self):
        cleaned_data = super().clean()
        query_name = cleaned_data.get("query_name")
        new_query_name = cleaned_data.get("new_query_name")

        if not query_name == 'Not Categorized' and new_query_name:
            raise ValidationError(
                    "If the query name is categorized new query name is not required."
                )
        if query_name == 'Not Categorized' and not new_query_name:
            raise ValidationError("Please provide new query name category.")

    class Meta:
        model = DataActionItem
        fields = '__all__'

class QueryNameForm(forms.ModelForm):

    class Meta:
        model = QueryName
        fields = '__all__'
