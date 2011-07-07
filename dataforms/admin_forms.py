from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from models import Binding, Field, FieldChoice


class BindingAdminForm(forms.ModelForm):
    parent_fields_select = forms.ModelMultipleChoiceField(queryset=Field.objects.all(), 
        widget=FilteredSelectMultiple("Parent Fields", is_stacked=False), required=False)
    parent_choices_select = forms.ModelMultipleChoiceField(queryset=FieldChoice.objects.all(), 
        widget=FilteredSelectMultiple("Parent Choices", is_stacked=False))
    children_select = forms.ModelMultipleChoiceField(queryset=Field.objects.all(), 
        widget=FilteredSelectMultiple("Children", is_stacked=False))
        
    def __init__(self, *args, **kwargs):
        super(BindingAdminForm, self).__init__(*args, **kwargs)
        self.fields['parent_fields_select'].initial = self.initial['parent_fields']
        self.fields['parent_choices_select'].initial = self.initial['parent_choices']
        self.fields['children_select'].initial = self.initial['children']
    
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
        
    