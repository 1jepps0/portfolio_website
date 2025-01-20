from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha import * 


class ContactForm(forms.Form):

    name = forms.CharField(
            label="Name",
            required=True,
            max_length=50,
            widget=forms.TextInput(attrs={"placeholder": "Name"})
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=70,
        widget=forms.TextInput(attrs={"placeholder": "Email"})
    )

    subject = forms.CharField(
        label="Subject",
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Subject"})
    )

    message = forms.CharField(
        label="Message",
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Message"})
    )

    captcha = ReCaptchaField(
        widget=widgets.ReCaptchaV3()
    )
