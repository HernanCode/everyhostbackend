from django import forms

class DockerForm(forms.Form):
    CHOICES = [
        ('1', 'Javascript'),
        ('2', 'Wordpress'),
    ]
    subdomain = forms.CharField(max_length=100)
    repository = forms.CharField(max_length=100)
    software = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    dbadmin = forms.CharField(max_length=100)
    dbpassword = forms.CharField(max_length=228)