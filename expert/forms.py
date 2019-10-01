from django import forms
from .models import *
from django.core.exceptions import ValidationError


def is_numeric(string):
    for ch in string:
        if ch in '0123456789':
            return True
    return False


class InitialInfoForm(forms.Form):
    first_name = forms.CharField(max_length=32, error_messages={'required': "نام نمی تواند خالی باشد."})
    last_name = forms.CharField(max_length=32, error_messages={'required': "نام خانوادگی نمی تواند خالی باشد."})
    special_field = forms.CharField(max_length=256, error_messages={'required': "حوزه تخصصی نمی تواند خالی باشد."})
    melli_code = forms.CharField(error_messages={'required': "کد ملی نمی تواند خالی باشد."})
    scientific_rank = forms.IntegerField(error_messages={'invalid': 'مرتبه علمی نباید خالی باشد!'})
    university = forms.CharField(max_length=128, error_messages={'required': "دانشگاه مورد نظر نمی تواند خالی باشد."})
    address = forms.CharField(widget=forms.Textarea(), error_messages={'required': "آدرس  نمی تواند خالی باشد."})
    home_number = forms.CharField(error_messages={'required': "شماره تلفن منزل نمی تواند خالی باشد."})
    phone_number = forms.CharField(error_messages={'required': "شماره تلفن همراه نمی تواند خالی باشد."})
    email_address = forms.EmailField(error_messages={'required': "ایمیل نمی تواند خالی باشد.",
                                                     'invalid': 'ایمیل وارد شده نامعتبر است.'})

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if is_numeric(first_name):
            raise forms.ValidationError('نام نباید شامل عدد باشد.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if is_numeric(last_name):
            raise forms.ValidationError('نام خانوادگی نباید شامل عدد باشد.')
        return last_name

    def clean_email_address(self):
        current_email = self.cleaned_data.get('email_address')
        try:
            ExpertUser.objects.get(user__username=current_email)
        except ExpertUser.DoesNotExist:
            raise forms.ValidationError('ایمیل وارد شده نادرست است.')

        return current_email

    def clean_melli_code(self):
        melli_code = self.cleaned_data.get('melli_code')
        print('mellicode:', melli_code)
        try:
            int(melli_code)
        except ValueError:
            raise forms.ValidationError('کد ملی باید یک عدد باشد.')

        if len(melli_code) != 10:
            raise forms.ValidationError('کد ملی باید ده رقمی باشد.')

        return melli_code

    def clean_home_number(self):
        home_number = self.cleaned_data.get('home_number')
        print('home_number:', home_number)
        try:
            int(home_number)
        except ValueError:
            raise forms.ValidationError('شماره تلفن منزل باید یک عدد باشد.')

        if len(home_number) != 11:
            raise forms.ValidationError('شماره تلفن منزل باید یازده رقمی باشد.')

        return home_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        print('phone_number:', phone_number)
        try:
            int(phone_number)
        except ValueError:
            raise forms.ValidationError('شماره تلفن همراه باید یک عدد باشد.')

        if len(phone_number) != 11:
            raise forms.ValidationError('شماره تلفن همراه باید یازده رقمی باشد.')

        return phone_number


class ExpertInfoForm(forms.ModelForm):
    prefix = 'expert_info'

    class Meta:
        model = ExpertForm
        exclude = ['eq_test']


class ScientificRecordForm(forms.ModelForm):
    class Meta:
        model = ScientificRecord
        fields = ['degree', 'major', 'university', 'city', 'date_of_graduation']

    def clean_date_of_graduation(self):
        year = self.cleaned_data.get('date_of_graduation')
        try:
            int(year)
        except ValueError:
            raise forms.ValidationError('سال اخذ مدرک باید عدد باشد.')
        return year


class ExecutiveRecordForm(forms.ModelForm):
    class Meta:
        model = ExecutiveRecord
        exclude = ['expert_form']


class ResearchRecordForm(forms.ModelForm):
    class Meta:
        model = ResearchRecord
        exclude = ['expert_form']


class PaperRecordForm(forms.ModelForm):
    class Meta:
        model = PaperRecord
        exclude = ['expert_form']

    def clean_citation(self):
        citation = self.cleaned_data.get('citation')
        try:
            int(citation)
        except ValueError:
            raise forms.ValidationError('تعداد ارجاع باید عدد باشد.')

        return citation


# class EQTestForm(forms.ModelForm):
#     class Meta:
#         model = EqTest
#         fields = '__all__'
#         widgets = {
#             'team_work': forms.RadioSelect()
#         }

class EQTestForm(forms.Form):
    INT_CHOICE = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    team_work = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 'group-work'}), choices=INT_CHOICE)

    # def __init__(self, *args, **kwargs):
    #     super(EQTestForm, self).__init__(*args, **kwargs)
    #     self.fields['team_work'].widget = forms.RadioSelect(attrs={
    #         'id': 'group-work'
    #     })