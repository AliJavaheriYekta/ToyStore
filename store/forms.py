from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from store.models import Media, Comment


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


class BrandForm(forms.Form):
    title = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Brand Title"}
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
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
        fields = ['product', 'media_type', 'file']

    def clean_file(self):
        media_type = self.cleaned_data.get('media_type')
        file = self.cleaned_data.get('file')

        if media_type == 'image':
            extensions = ['jpg', 'jpeg', 'png', 'gif']
            validator = FileExtensionValidator(allowed_extensions=extensions)
            validator(file)  # Raise ValidationError if not an image
        elif media_type == 'video':
            extensions = ['mp4']
            validator = FileExtensionValidator(allowed_extensions=extensions)
            validator(file)  # Raise ValidationError if not a video
        else:
            raise ValidationError('Invalid media type.')

        return file


class CommentAdminForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['product', 'user', 'content', 'is_active']
