from edc_base.modeladmin.admin import BaseModelAdmin


class BaseAdmin(BaseModelAdmin):

    def __init__(self, *args, **kwargs):
        super(BaseAdmin, self).__init__(*args, **kwargs)
        self.search_fields = ['subject', 'comment', 'rt']
        self.list_display = [
            'created', 'subject', 'rt', 'status', 'user_created', 'user_modified', 'modified'
        ]
        self.list_filter = ['status', 'created', 'user_created', 'modified', 'user_modified']
