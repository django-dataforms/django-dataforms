# encoding: utf-8
#@PydevCodeAnalysisIgnore
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'AnswerChoice'
        db.delete_table('dataforms_answerchoice')

        # Deleting model 'AnswerText'
        db.delete_table('dataforms_answertext')

        # Deleting model 'AnswerNumber'
        db.delete_table('dataforms_answernumber')

        # Adding field 'Answer.choice'
        db.add_column('dataforms_answer', 'choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Choice'], null=True, blank=True), keep_default=False)

        # Adding unique constraint on 'Choice', fields ['value', 'title']
        db.create_unique('dataforms_choice', ['value', 'title'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Choice', fields ['value', 'title']
        db.delete_unique('dataforms_choice', ['value', 'title'])

        # Adding model 'AnswerChoice'
        db.create_table('dataforms_answerchoice', (
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Answer'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Choice'])),
        ))
        db.send_create_signal('dataforms', ['AnswerChoice'])

        # Adding model 'AnswerText'
        db.create_table('dataforms_answertext', (
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Answer'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('dataforms', ['AnswerText'])

        # Adding model 'AnswerNumber'
        db.create_table('dataforms_answernumber', (
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Answer'])),
            ('num', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('dataforms', ['AnswerNumber'])

        # Deleting field 'Answer.choice'
        db.delete_column('dataforms_answer', 'choice_id')


    models = {
        'dataforms.answer': {
            'Meta': {'object_name': 'Answer'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Choice']", 'null': 'True', 'blank': 'True'}),
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Submission']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'Meta': {'ordering': "['title']", 'unique_together': "(('title', 'value'),)", 'object_name': 'Choice'},
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
