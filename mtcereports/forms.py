from django import forms


FORMAT_CHOICES = (
    ('xls', 'xls'),
    ('csv', 'csv'),
    ('json', 'json'),
)

class FormatFrom(forms.Form):
    format = forms.ChoiceField(choices = FORMAT_CHOICES, widget=forms.Select(attrs={'class':'form-select'}))