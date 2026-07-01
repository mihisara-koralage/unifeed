from django import forms
from .models import Resource
import re

class ResourceForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. CS3012 Past Papers 2022',
        })
    )
    url = forms.URLField(
        max_length=500,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://drive.google.com/...',
        })
    )
    category = forms.ChoiceField(
        choices=Resource.Category.choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    description = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Optional: briefly describe what this contains',
        })
    )

    class Meta:
        model  = Resource
        fields = ('title', 'url', 'category', 'description')

    def clean_url(self):
        url = self.cleaned_data.get('url', '').strip()

        # Regex: must start with http:// or https:// followed by a valid domain
        pattern = re.compile(
            r'^https?://'                      # http:// or https://
            r'(([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,})'  # domain
            r'(/[^\s]*)?$'                     # optional path
        )

        if not pattern.match(url):
            raise forms.ValidationError(
                'Please enter a valid URL starting with http:// or https://'
            )

        # Block obviously bad schemes just in case
        if url.startswith('javascript:') or url.startswith('data:'):
            raise forms.ValidationError('This URL type is not allowed.')

        return url