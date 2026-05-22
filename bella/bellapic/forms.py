from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media_file', 'post_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'media_file': forms.FileInput(attrs={'class': 'form-control'}),
            'post_type': forms.Select(attrs={'class': 'form-select'})
        }


# To ensure the forms in the popups are also clean,
# you can use these classes to remove extra text/placeholders
class CleanLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': ''})

class CleanSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': ''})
