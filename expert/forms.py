from django import forms


class InitialInfoForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    special_field = forms.CharField(max_length=256)
    melli_code = forms.IntegerField()
    scientific_rank = forms.IntegerField()
    university = forms.CharField(max_length=128)
    address = forms.CharField(widget=forms.Textarea())
    home_number = forms.IntegerField()
    phone_number = forms.IntegerField()
    email_address = forms.EmailField()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name
