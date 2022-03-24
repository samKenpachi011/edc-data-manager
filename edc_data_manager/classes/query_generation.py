from django.apps import apps as django_apps
from django.db.models import Q

from edc_appointment.constants import COMPLETE_APPT


class QueryGeneration:

    antenatal_enrollment_model = 'flourish_caregiver.antenatalenrollment'
    maternal_delivery_model = 'flourish_caregiver.maternaldelivery'

    @property
    def antenatal_enrollment_model_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)
    
    @property
    def maternal_delivery_model_cls(self):
        return django_apps.get_model(self.maternal_delivery_model)

    @property
    def query_name(self):
        return django_apps.get_model('edc_data_manager.queryname')

    @property
    def action_item_cls(self):
        return django_apps.get_model('edc_data_manager.dataactionitem')

    def create_query_name(self, query_name=None):
        query = None
        try:
            query = self.query_name.objects.get(query_name=query_name)
        except self.query_name.DoesNotExist:
            query = self.query_name.objects.create(query_name=query_name)
        return query


    def create_action_item(
            self, site=None, subject_identifier=None, query_name=None,
            assign=None, subject=None, comment=None):
        try:
            self.action_item_cls.objects.get(
                subject_identifier=subject_identifier,
                query_name=query_name
            )
        except self.action_item_cls.DoesNotExist:
            self.action_item_cls.objects.create(
                subject_identifier=subject_identifier,
                query_name=query_name,
                assigned=assign,
                subject=subject,
                comment=comment,
                site=site
            )

    def check_appt_status(self, required_crf=None):
        appointment_model_cls = django_apps.get_model(
            required_crf.schedule.appointment_model)
        try:
            appt = appointment_model_cls.objects.get(
                subject_identifier=required_crf.subject_identifier,
                visit_code=required_crf.visit_code,
                visit_code_sequence=required_crf.visit_code_sequence,
                schedule_name=required_crf.schedule_name)
        except appointment_model_cls.DoesNotExist:
            return False
        else:
            return False if appt.appt_status == COMPLETE_APPT else True

    @property
    def missing_visit_forms(self):
        """
        Missing CRF data
        """
        crfmetadata = django_apps.get_model('edc_metadata.crfmetadata')
        query = self.create_query_name(
            query_name='Missing Visit Forms data')
        
        maternal_identifier = self.maternal_delivery_model_cls.objects.all().values_list(
            'subject_identifier', flat=True)
        antenatal_identifiers = self.antenatal_enrollment_model_cls.objects.all().values_list(
            'subject_identifier', flat=True)
        enrolled_identifiers = list(set(antenatal_identifiers)) + list(set(maternal_identifier))
        
        required_crfs = crfmetadata.objects.filter(
            subject_identifier__in=enrolled_identifiers, entry_status='REQUIRED')
        data = [(qs.subject_identifier, qs.schedule_name, qs.visit_code,
                 qs.visit_code_sequence, qs.verbose_name) for qs in required_crfs if self.check_appt_status(qs)]
        for missing_crf in required_crfs:
            assign = 'clinic'
            model = missing_crf.model
            model = model.split('.')[1]
            subject = f"Participant is missing {model} data for visit {missing_crf.visit_code}."
            comment = subject + " Please complete the missing data for the form"
            self.create_action_item(
                subject_identifier=missing_crf.subject_identifier,
                query_name=query.query_name,
                assign=assign,
                subject=subject,
                comment=comment
            )
