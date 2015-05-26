from collections import OrderedDict

from django.contrib import admin
from django.apps import apps

from ..models import DataDictionaryModel


class DataDictionary(object):

    def __init__(self, app_label):
        self.app_label = app_label
        self.app = apps.get_app(app_label)
        self.models = apps.get_models(self.app)

    @property
    def dictionary(self):
        """
        { app_label.model_name:
            {model: {'db_table': '<table_name>', ...},
             fields: {'prompt': verbose_name, ...}
            }
        }

        app_label, model_name, db_table, field, db_field, prompt,
        type, max_length, default, null, blank, editable, help_text,
        encrypted, choices, primary_key, unique

        """
        self._dictionary = []
        for model in self.models:
            # find admin class
            if 'audit' not in model._meta.object_name.lower():
                for model_admin in admin.sites.site._registry.values():
                    if model_admin.model == model:
                        break
                for field in model._meta.fields:
                    row = OrderedDict(
                        app_label=self.app_label,
                        model_name=model._meta.object_name,
                        db_table=model._meta.db_table,
                    )
                    row.update(in_admin=False)
                    if model_admin:
                        row.update(in_admin=True)
                        # get the question number
                        row.update(number=None)
                        if model_admin.fields:
                            for index, fld in enumerate(model_admin.fields):
                                if field.name == fld:
                                    row.update(number=index + 1)
                                    break
                    row.update(
                        field=field.name,
                        db_field=field.attname,
                        type=field.get_internal_type(),
                        max_length=field.max_length,
                    )
                    prompt = field.verbose_name
                    if not prompt.startswith == '"':
                        prompt = '"' + prompt
                    if not prompt.endswith == '"':
                        prompt = prompt + '"'
                    row.update(prompt=prompt)
                    try:
                        default = field.default.func_name
                    except:
                        pass
                    try:
                        default = field.default.split('.')[-1]
                    except:
                        pass
                    try:
                        default = field.default
                    except:
                        default = field.default
                    row.update(default=default)
                    row.update(
                        default=field.default,
                        null=field.null,
                        blank=field.blank,
                        editable=field.editable,
                        help_text=field.help_text,
                    )
                    if 'encrypt' in dir(field):
                        encrypted = True
                    else:
                        encrypted = False
                    row.update(encrypted=encrypted)
                    if field.choices:
                        choices = field.choices
                    else:
                        choices = ''
                    row.update(
                        choices=choices,
                        primary_key=field.primary_key,
                        unique=field._unique,
                    )
                    self._dictionary.append(row)
        return self._dictionary

    def save(self):
        DataDictionaryModel.objects.filter(app_label=self.app_label).delete()
        for row in self.dictionary:
            DataDictionaryModel.objects.create(**row)
