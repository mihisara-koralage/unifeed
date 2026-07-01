from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Canon EOS M50 Camera',
        })
    )
    description = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe the item — age, any defects, what is included...',
        })
    )
    price = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'min': '0',
        })
    )
    category = forms.ChoiceField(
        choices=Listing.Category.choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    condition = forms.ChoiceField(
        choices=Listing.Condition.choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Main Gate, Library Entrance',
        })
    )
    contact_info = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. 07X XXX XXXX or your email',
        })
    )
    # Three separate image fields — kept simple and explicit
    image_1 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    image_2 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    image_3 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    class Meta:
        model  = Listing
        fields = ('title', 'description', 'price', 'category', 'condition', 'location', 'contact_info')


class ReportForm(forms.Form):
    reason = forms.ChoiceField(
        choices=[(r.value, r.label) for r in __import__('marketplace.models', fromlist=['Report']).Report.Reason],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    details = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional: add more details about the issue',
        })
    )