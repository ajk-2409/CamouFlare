from django import forms
from django.core.exceptions import ValidationError


def validate_png(value):
    if not value.name.lower().endswith(".png"):
        raise ValidationError("Only PNG files are allowed.")


class EncodeForm(forms.Form):
    image = forms.ImageField(label="Select Image", validators=[validate_png])
    message = forms.CharField(
        widget=forms.Textarea, label="Enter Message", required=False
    )


class DecodeForm(forms.Form):
    image = forms.ImageField(label="Select Image")
