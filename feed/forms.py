from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': "What's happening on campus? Use #hashtags",
            'rows': 3,
            'class': 'form-control',
        }),
        max_length=1000,
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )

    class Meta:
        model  = Post
        fields = ('content', 'image')