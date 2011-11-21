# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Condition'
        db.create_table('dataforms_condition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.DataForm'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Field'])),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('dataforms', ['Condition'])

        # Adding M2M table for field true_field on 'Condition'
        db.create_table('dataforms_condition_true_field', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('condition', models.ForeignKey(orm['dataforms.condition'], null=False)),
            ('field', models.ForeignKey(orm['dataforms.field'], null=False))
        ))
        db.create_unique('dataforms_condition_true_field', ['condition_id', 'field_id'])

        # Adding M2M table for field true_choice on 'Condition'
        db.create_table('dataforms_condition_true_choice', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('condition', models.ForeignKey(orm['dataforms.condition'], null=False)),
            ('choice', models.ForeignKey(orm['dataforms.choice'], null=False))
        ))
        db.create_unique('dataforms_condition_true_choice', ['condition_id', 'choice_id'])

        # Adding M2M table for field false_field on 'Condition'
        db.create_table('dataforms_condition_false_field', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('condition', models.ForeignKey(orm['dataforms.condition'], null=False)),
            ('field', models.ForeignKey(orm['dataforms.field'], null=False))
        ))
        db.create_unique('dataforms_condition_false_field', ['condition_id', 'field_id'])

        # Adding M2M table for field false_choice on 'Condition'
        db.create_table('dataforms_condition_false_choice', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('condition', models.ForeignKey(orm['dataforms.condition'], null=False)),
            ('choice', models.ForeignKey(orm['dataforms.choice'], null=False))
        ))
        db.create_unique('dataforms_condition_false_choice', ['condition_id', 'choice_id'])


    def backwards(self, orm):
        
        # Deleting model 'Condition'
        db.delete_table('dataforms_condition')

        # Removing M2M table for field true_field on 'Condition'
        db.delete_table('dataforms_condition_true_field')

        # Removing M2M table for field true_choice on 'Condition'
        db.delete_table('dataforms_condition_true_choice')

        # Removing M2M table for field false_field on 'Condition'
        db.delete_table('dataforms_condition_false_field')

        # Removing M2M table for field false_choice on 'Condition'
        db.delete_table('dataforms_condition_false_choice')


    models = {
        'dataforms.answer': {
            'Meta': {'object_name': 'Answer'},
            'choice': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['dataforms.Choice']", 'null': 'True', 'blank': 'True'}),
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Submission']"}),
            'value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
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
        'dataforms.condition': {
            'Meta': {'object_name': 'Condition'},
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']"}),
            'false_choice': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'false_choice_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['dataforms.Choice']"}),
            'false_field': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'false_field_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['dataforms.Field']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'true_choice': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'true_choice_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['dataforms.Choice']"}),
            'true_field': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'true_field_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['dataforms.Field']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
