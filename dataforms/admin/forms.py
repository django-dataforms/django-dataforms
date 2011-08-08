from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from dataforms.models import Binding, Field, FieldChoice, DataFormField

FIELD_CHOICES = [
    (u'%s__%s' % (field.data_form, field.field), u'%s (%s)' % (field.data_form, field.field)) 
    for field in DataFormField.objects.select_related('data_form', 'field').all().order_by('data_form')
]

CHOICE_CHOICES = [
    (u'%s__%s___%s' % (fc.data_form_slug, fc.field_slug, fc.choice_value), 
     u'(%s) %s (%s)' % (fc.data_form_slug, fc.field_slug, fc.choice_value.upper())) 
    for fc in FieldChoice.objects.get_fieldchoice_data()
]

class BindingAdminForm(forms.ModelForm):
#    field_choice = forms.ModelChoiceField(
#        queryset=FieldChoice.objects.select_related('field', 'choice').all(), required=False
#    )
    true_field = forms.MultipleChoiceField(choices=FIELD_CHOICES, 
        widget=FilteredSelectMultiple("True Fields", is_stacked=False), required=False)
    true_choice = forms.MultipleChoiceField(choices=CHOICE_CHOICES,
        widget=FilteredSelectMultiple("True Choices", is_stacked=False), required=False)
    false_field = forms.MultipleChoiceField(choices=FIELD_CHOICES,
        widget=FilteredSelectMultiple("False Fields", is_stacked=False), required=False)
    false_choice = forms.MultipleChoiceField(choices=CHOICE_CHOICES,
        widget=FilteredSelectMultiple("False Choices", is_stacked=False), required=False)

    additional_rules = forms.ModelMultipleChoiceField(queryset=Binding.objects.all(), required=False)
    
    def clean_additional_rules(self):
        data = ','.join([unicode(b.id) for b in self.cleaned_data['additional_rules']])
        return data
        
    
    class Meta:
        model = Binding


class FieldAdminForm(forms.ModelForm):
    class Meta:
        model = Field
        
    def clean_label(self):
        data = self.cleaned_data['label']

        if 'meta' in data:
            raise forms.ValidationError("You cannot use the term 'meta' as a label as it is reserved.")
        return data        
        
    
