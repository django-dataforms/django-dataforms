# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BindingChoice'
        db.create_table('dataforms_bindingchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('binding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Binding'])),
            ('field_choice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.FieldChoice'])),
            ('data_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.DataForm'])),
            ('is_true', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('dataforms', ['BindingChoice'])

        # Adding model 'BindingField'
        db.create_table('dataforms_bindingfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('binding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Binding'])),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.Field'])),
            ('data_form', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataforms.DataForm'])),
            ('is_true', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('dataforms', ['BindingField'])

        # Removing M2M table for field false_field on 'Binding'
        db.delete_table('dataforms_binding_false_field')

        # Removing M2M table for field true_choice on 'Binding'
        db.delete_table('dataforms_binding_true_choice')

        # Removing M2M table for field true_field on 'Binding'
        db.delete_table('dataforms_binding_true_field')

        # Removing M2M table for field false_choice on 'Binding'
        db.delete_table('dataforms_binding_false_choice')


    def backwards(self, orm):
        
        # Deleting model 'BindingChoice'
        db.delete_table('dataforms_bindingchoice')

        # Deleting model 'BindingField'
        db.delete_table('dataforms_bindingfield')

        # Adding M2M table for field false_field on 'Binding'
        db.create_table('dataforms_binding_false_field', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('binding', models.ForeignKey(orm['dataforms.binding'], null=False)),
            ('field', models.ForeignKey(orm['dataforms.field'], null=False))
        ))
        db.create_unique('dataforms_binding_false_field', ['binding_id', 'field_id'])

        # Adding M2M table for field true_choice on 'Binding'
        db.create_table('dataforms_binding_true_choice', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('binding', models.ForeignKey(orm['dataforms.binding'], null=False)),
            ('fieldchoice', models.ForeignKey(orm['dataforms.fieldchoice'], null=False))
        ))
        db.create_unique('dataforms_binding_true_choice', ['binding_id', 'fieldchoice_id'])

        # Adding M2M table for field true_field on 'Binding'
        db.create_table('dataforms_binding_true_field', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('binding', models.ForeignKey(orm['dataforms.binding'], null=False)),
            ('field', models.ForeignKey(orm['dataforms.field'], null=False))
        ))
        db.create_unique('dataforms_binding_true_field', ['binding_id', 'field_id'])

        # Adding M2M table for field false_choice on 'Binding'
        db.create_table('dataforms_binding_false_choice', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('binding', models.ForeignKey(orm['dataforms.binding'], null=False)),
            ('fieldchoice', models.ForeignKey(orm['dataforms.fieldchoice'], null=False))
        ))
        db.create_unique('dataforms_binding_false_choice', ['binding_id', 'fieldchoice_id'])


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
        'dataforms.binding': {
            'Meta': {'object_name': 'Binding'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'action_field': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'action_field_set'", 'to': "orm['dataforms.Field']", 'through': "orm['dataforms.BindingField']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'actoin_choice': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'action_choice_set'", 'to': "orm['dataforms.FieldChoice']", 'through': "orm['dataforms.BindingChoice']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']", 'null': 'True', 'blank': 'True'}),
            'field_choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.FieldChoice']", 'null': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'parent': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'dataforms.bindingchoice': {
            'Meta': {'object_name': 'BindingChoice'},
            'binding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Binding']"}),
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']"}),
            'field_choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.FieldChoice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_true': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'dataforms.bindingfield': {
            'Meta': {'object_name': 'BindingField'},
            'binding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Binding']"}),
            'data_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.DataForm']"}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataforms.Field']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_true': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
