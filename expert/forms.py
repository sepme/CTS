from django import forms
from .models import ExpertForm


class InitialInfoForm(forms.Form):
    first_name = forms.CharField(max_length=32, required=False)
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
        first_name = self.cleaned_data.get('first_name')
        print("errors", self.errors)
        if first_name is None or first_name == '':

            raise forms.ValidationError("نام نمی تواند خالی باشد.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        print(last_name)
        if last_name is None or last_name == '':

            raise forms.ValidationError('نام خانوادگی نمی تواند خالی باشد.')

        return last_name

    def clean_email_address(self):
        current_email = self.cleaned_data.get('email_address')
        email = ExpertForm.objects.filter(email_address=current_email)
        if email.exists():
            raise forms.ValidationError('کاربر با این ایمیل قبلا ثبت نام شده است')

        return current_email

    def clean_melli_code(self):
        melli_code = self.cleaned_data.get('melli_code')

        if len(str(melli_code)) != 10:
            raise forms.ValidationError('code melli eshteabbahe')
        return melli_code

    def clean_home_number(self):
        home_number = self.cleaned_data.get('home_number')
        if len(str(home_number)) != 10:
            raise forms.ValidationError('شماره تلفن منزل باید ده رقمی باشد.')
        return home_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number)) != 10:
            raise forms.ValidationError('شماره تلفن همراه باید یازده رقمی باشد.')
        return phone_number

