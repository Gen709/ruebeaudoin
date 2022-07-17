from django import forms


class UrlForm(forms.Form):
    url_name = forms.URLField(label="Recepy URL", max_length=300)