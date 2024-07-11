from django import forms
from django.forms import Form


class GenerateBlogForm(Form):
    title = forms.CharField(max_length=200)
    AUTOBLOG_DEMO_API_KEY = forms.CharField(max_length=200)
    class Meta:
        fields = ["title", "AUTOBLOG_DEMO_API_KEY"]