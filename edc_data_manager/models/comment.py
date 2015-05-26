from datetime import date
from django.db import models
from django_crypto_fields.fields import EncryptedTextField

from edc_base.model.models import BaseModel


class Comment(BaseModel):

    subject = models.CharField(max_length=50)
    comment_date = models.DateField(default=date.today())
    comment = EncryptedTextField(max_length=500)
    rt = models.IntegerField(default=0, verbose_name='RT Ref.')
    status = models.CharField(
        max_length=35,
        choices=(('Open', 'Open'), ('Stalled', 'Stalled'), ('Resolved', 'Resolved')),
        default='Open')
    objects = models.Manager()

    class Meta:
        app_label = "data_manager"
