from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from models import Condition, Field, FieldChoice

FIELD_QS = Field.objects.all()
CHOICE_QS = FieldChoice.objects.all()

class ConditionAdminForm(forms.ModelForm):
    true_field = forms.ModelMultipleChoiceField(queryset=FIELD_QS, 
        widget=FilteredSelectMultiple("True Fields", is_stacked=False), required=False)
    true_choice = forms.ModelMultipleChoiceField(queryset=CHOICE_QS, 
        widget=FilteredSelectMultiple("True Choices", is_stacked=False), required=False)
    false_field = forms.ModelMultipleChoiceField(queryset=FIELD_QS, 
        widget=FilteredSelectMultiple("False Fields", is_stacked=False), required=False)
    false_choice = forms.ModelMultipleChoiceField(queryset=CHOICE_QS, 
        widget=FilteredSelectMultiple("False Choices", is_stacked=False), required=False)
            
#    def __init__(self, *args, **kwargs):
#        super(ConditionAdminForm, self).__init__(*args, **kwargs)
#        if self.initial:
#            self.fields['true_field_select'].initial = self.initial['true_field']
#            self.fields['true_choice_select'].initial = self.initial['true_choice']
#            self.fields['false_field_select'].initial = self.initial['false_field']
#            self.fields['false_choice_select'].initial = self.initial['false_choice']
    
#    def clean(self):
#        cleaned_data = self.cleaned_data
#
#        if not cleaned_data['parent_fields_select'] and not cleaned_data['parent_choices_select']:
#            raise forms.ValidationError("A Parent Field or Parent Choice is required.")
#
#        return cleaned_data
    
    
    class Meta:
        model = Condition
        #exclude = ('true_field', 'true_choice', 'false_field', 'false_choice',)


class FieldAdminForm(forms.ModelForm):
    class Meta:
        model = Field
        
    def clean_label(self):
        data = self.cleaned_data['label']

        if 'meta' in data:
            raise forms.ValidationError("You cannot use the term 'meta' as a label as it is reserved.")
        return data        
        
    