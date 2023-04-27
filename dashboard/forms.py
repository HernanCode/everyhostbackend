from django import forms

class ServiceForm(forms.Form):
    CHOICES = [
        ('nc', 'Nextcloud'),
        ('wp', 'Wordpress'),
        ('mysql', 'MySQL'),
    ]
    subdomain = forms.CharField(max_length=100)
    repository = forms.CharField(max_length=100)
    software = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    dbadmin = forms.CharField(max_length=100)
    dbpassword = forms.CharField(max_length=228)