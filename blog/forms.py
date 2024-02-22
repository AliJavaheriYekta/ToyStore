from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from blog.models import Media


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['file']
        widgets = {
            'file': forms.MultipleHiddenInput(attrs={'multiple': True}),
        }
        validators = [FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4'])]


class RestrictedFileExtensionValidator:
    def __init__(self, allowed_extensions):
        self.allowed_extensions = allowed_extensions

    def __call__(self, value):
        extension = value.name.split('.')[-1].lower()
        if extension not in self.allowed_extensions:
            raise ValidationError(
                f"Unsupported file extension. Allowed extensions are: {', '.join(self.allowed_extensions)}.")


class MediaAdminForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['post', 'media_type', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        validator = RestrictedFileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4'])
        validator(file)
        return file
