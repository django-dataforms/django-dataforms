# encoding: utf-8
#@PydevCodeAnalysisIgnore
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Collection'
        db.create_table('dataforms_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('dataforms', ['Collection'])

        # Adding model 'CollectionDataForm'
        db.create_table('dataforms_collectiondataform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Collection'], null=True)),
            ('data_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.DataForm'], null=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Section'], null=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('dataforms', ['CollectionDataForm'])

        # Adding unique constraint on 'CollectionDataForm', fields ['collection', 'data_form']
        db.create_unique('dataforms_collectiondataform', ['collection_id', 'data_form_id'])

        # Adding model 'CollectionVersion'
        db.create_table('dataforms_collectionversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Collection'])),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('dataforms', ['CollectionVersion'])

        # Adding model 'Section'
        db.create_table('dataforms_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal('dataforms', ['Section'])

        # Adding model 'DataForm'
        db.create_table('dataforms_dataform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('dataforms', ['DataForm'])

        # Adding model 'DataFormField'
        db.create_table('dataforms_dataformfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.DataForm'], null=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Field'], null=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('dataforms', ['DataFormField'])

        # Adding unique constraint on 'DataFormField', fields ['data_form', 'field']
        db.create_unique('dataforms_dataformfield', ['data_form_id', 'field_id'])

        # Adding model 'Field'
        db.create_table('dataforms_field', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('help_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('initial', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('arguments', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('dataforms', ['Field'])

        # Adding model 'Binding'
        db.create_table('dataforms_binding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.DataForm'])),
        ))
        db.send_create_signal('dataforms', ['Binding'])

        # Adding model 'ParentField'
        db.create_table('dataforms_parentfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('binding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Binding'])),
            ('parent_field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Field'])),
        ))
        db.send_create_signal('dataforms', ['ParentField'])

        # Adding model 'ParentFieldChoice'
        db.create_table('dataforms_parentfieldchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('binding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Binding'])),
            ('field_choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.FieldChoice'])),
        ))
        db.send_create_signal('dataforms', ['ParentFieldChoice'])

        # Adding model 'ChildField'
        db.create_table('dataforms_childfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('binding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Binding'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Field'])),
        ))
        db.send_create_signal('dataforms', ['ChildField'])

        # Adding model 'FieldChoice'
        db.create_table('dataforms_fieldchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Field'], null=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Choice'], null=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('dataforms', ['FieldChoice'])

        # Adding unique constraint on 'FieldChoice', fields ['field', 'choice']
        db.create_unique('dataforms_fieldchoice', ['field_id', 'choice_id'])

        # Adding model 'Choice'
        db.create_table('dataforms_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('dataforms', ['Choice'])

        # Adding model 'Submission'
        db.create_table('dataforms_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, db_index=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Collection'], null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('dataforms', ['Submission'])

        # Adding model 'AnswerChoice'
        db.create_table('dataforms_answerchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Answer'])),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Choice'])),
        ))
        db.send_create_signal('dataforms', ['AnswerChoice'])

        # Adding model 'AnswerText'
        db.create_table('dataforms_answertext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Answer'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('dataforms', ['AnswerText'])

        # Adding model 'AnswerNumber'
        db.create_table('dataforms_answernumber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Answer'])),
            ('num', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('dataforms', ['AnswerNumber'])

        # Adding model 'Answer'
        db.create_table('dataforms_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Submission'])),
            ('data_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.DataForm'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Field'])),
        ))
        db.send_create_signal('dataforms', ['Answer'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FieldChoice', fields ['field', 'choice']
        db.delete_unique('dataforms_fieldchoice', ['field_id', 'choice_id'])

        # Removing unique constraint on 'DataFormField', fields ['data_form', 'field']
        db.delete_unique('dataforms_dataformfield', ['data_form_id', 'field_id'])

        # Removing unique constraint on 'CollectionDataForm', fields ['collection', 'data_form']
        db.delete_unique('dataforms_collectiondataform', ['collection_id', 'data_form_id'])

        # Deleting model 'Collection'
        db.delete_table('dataforms_collection')

        # Deleting model 'CollectionDataForm'
        db.delete_table('dataforms_collectiondataform')

        # Deleting model 'CollectionVersion'
        db.delete_table('dataforms_collectionversion')

        # Deleting model 'Section'
        db.delete_table('dataforms_section')

        # Deleting model 'DataForm'
        db.delete_table('dataforms_dataform')

        # Deleting model 'DataFormField'
        db.delete_table('dataforms_dataformfield')

        # Deleting model 'Field'
        db.delete_table('dataforms_field')

        # Deleting model 'Binding'
        db.delete_table('dataforms_binding')

        # Deleting model 'ParentField'
        db.delete_table('dataforms_parentfield')

        # Deleting model 'ParentFieldChoice'
        db.delete_table('dataforms_parentfieldchoice')

        # Deleting model 'ChildField'
        db.delete_table('dataforms_childfield')

        # Deleting model 'FieldChoice'
        db.delete_table('dataforms_fieldchoice')

        # Deleting model 'Choice'
        db.delete_table('dataforms_choice')

        # Deleting model 'Submission'
        db.delete_table('dataforms_submission')

        # Deleting model 'AnswerChoice'
        db.delete_table('dataforms_answerchoice')

        # Deleting model 'AnswerText'
        db.delete_table('dataforms_answertext')

        # Deleting model 'AnswerNumber'
        db.delete_table('dataforms_answernumber')

        # Deleting model 'Answer'
        db.delete_table('dataforms_answer')


    models = {
        'dataforms.answer': {
            'Meta': {'object_name': 'Answer'},
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Submission']"})
        },
        'dataforms.answerchoice': {
            'Meta': {'object_name': 'AnswerChoice'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Answer']"}),
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Choice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'dataforms.answernumber': {
            'Meta': {'object_name': 'AnswerNumber'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Answer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {})
        },
        'dataforms.answertext': {
            'Meta': {'object_name': 'AnswerText'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Answer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'dataforms.binding': {
            'Meta': {'object_name': 'Binding'},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dataforms.Field']", 'through': "orm['dataforms.ChildField']", 'symmetrical': 'False'}),
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_choices': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'choices_set'", 'symmetrical': 'False', 'through': "orm['dataforms.ParentFieldChoice']", 'to': "orm['dataforms.FieldChoice']"}),
            'parent_fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fields_set'", 'symmetrical': 'False', 'through': "orm['dataforms.ParentField']", 'to': "orm['dataforms.Field']"})
        },
        'dataforms.childfield': {
            'Meta': {'object_name': 'ChildField'},
            'binding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Binding']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'dataforms.choice': {
            'Meta': {'ordering': "['title']", 'object_name': 'Choice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'dataforms.collection': {
            'Meta': {'object_name': 'Collection'},
            'data_forms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dataforms.DataForm']", 'through': "orm['dataforms.CollectionDataForm']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'dataforms.collectiondataform': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('collection', 'data_form'),)", 'object_name': 'CollectionDataForm'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Collection']", 'null': 'True'}),
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Section']", 'null': 'True'})
        },
        'dataforms.collectionversion': {
            'Meta': {'object_name': 'CollectionVersion'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'dataforms.dataform': {
            'Meta': {'ordering': "['title']", 'object_name': 'DataForm'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dataforms.Field']", 'through': "orm['dataforms.DataFormField']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'dataforms.dataformfield': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('data_form', 'field'),)", 'object_name': 'DataFormField'},
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']", 'null': 'True'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'dataforms.field': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Field'},
            'arguments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'choices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dataforms.Choice']", 'through': "orm['dataforms.FieldChoice']", 'symmetrical': 'False'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'help_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'dataforms.fieldchoice': {
            'Meta': {'ordering': "['field', 'order']", 'unique_together': "(('field', 'choice'),)", 'object_name': 'FieldChoice'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Choice']", 'null': 'True'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'dataforms.parentfield': {
            'Meta': {'object_name': 'ParentField'},
            'binding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Binding']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']"})
        },
        'dataforms.parentfieldchoice': {
            'Meta': {'object_name': 'ParentFieldChoice'},
            'binding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Binding']"}),
            'field_choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.FieldChoice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'dataforms.section': {
            'Meta': {'ordering': "['title']", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'dataforms.submission': {
            'Meta': {'object_name': 'Submission'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Collection']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['dataforms']
