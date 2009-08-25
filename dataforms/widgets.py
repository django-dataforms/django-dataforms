from django import forms

class NoteWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return ""