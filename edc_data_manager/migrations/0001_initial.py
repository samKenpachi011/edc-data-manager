# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table('bhp_data_manager_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac2-2.local', max_length=50)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comment_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2016, 1, 9, 0, 0))),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('rt', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Open', max_length=35)),
        ))
        db.send_create_signal('data_manager', ['Comment'])

        # Adding model 'ActionItem'
        db.create_table('bhp_data_manager_actionitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac2-2.local', max_length=50)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['edc_registration.RegisteredSubject'])),
            ('subject', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('action_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2016, 1, 9, 0, 0))),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2016, 4, 8, 0, 0))),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('display_on_dashboard', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('rt', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('action_priority', self.gf('django.db.models.fields.CharField')(default='Normal', max_length=35)),
            ('action_group', self.gf('django.db.models.fields.CharField')(default='no group', max_length=35)),
            ('status', self.gf('django.db.models.fields.CharField')(default='open', max_length=35)),
        ))
        db.send_create_signal('data_manager', ['ActionItem'])


    def backwards(self, orm):
        # Deleting model 'Comment'
        db.delete_table('bhp_data_manager_comment')

        # Deleting model 'ActionItem'
        db.delete_table('bhp_data_manager_actionitem')


    models = {
        'data_manager.actionitem': {
            'Meta': {'object_name': 'ActionItem', 'db_table': "'bhp_data_manager_actionitem'"},
            'action_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2016, 1, 9, 0, 0)'}),
            'action_group': ('django.db.models.fields.CharField', [], {'default': "'no group'", 'max_length': '35'}),
            'action_priority': ('django.db.models.fields.CharField', [], {'default': "'Normal'", 'max_length': '35'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_on_dashboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2016, 4, 8, 0, 0)'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac2-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['edc_registration.RegisteredSubject']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'rt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '35'}),
            'subject': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'data_manager.comment': {
            'Meta': {'object_name': 'Comment', 'db_table': "'bhp_data_manager_comment'"},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'comment_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2016, 1, 9, 0, 0)'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac2-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'rt': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Open'", 'max_length': '35'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'edc_registration.registeredsubject': {
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(('first_name', 'dob', 'initials', 'additional_key'),)", 'object_name': 'RegisteredSubject'},
            'additional_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '36', 'null': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dm_comment': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac2-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'randomization_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_identifier': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relative_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'screening_age_in_years': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'screening_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'screening_identifier': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subject_consent_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_aka': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'survival_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['data_manager']