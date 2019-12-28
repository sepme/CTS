from django import forms
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from . import models


class IndustryBasicInfoForm(forms.Form):
    photo = forms.FileField(required=False)
    name = forms.CharField(max_length=300, required=False)
    registration_number = forms.CharField(max_length=50, required=False)
    date_of_foundation = forms.CharField(max_length=50, required=False)
    research_field = forms.CharField(max_length=300, required=True,
                                     error_messages={'required': 'حوزه فعالیت را وارد کنید'})
    industry_type = forms.IntegerField(error_messages={'invalid': 'لطفا نوع شرکت را انتخاب کنید.'})
    industry_address = forms.CharField(max_length=3000)
    phone_number = forms.CharField(max_length=15)
    email_address = forms.EmailField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_photo(self):
        data = self.cleaned_data["photo"]
        return data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name is None or name == '':
            raise ValidationError(_("نام نمی تواند خالی باشد."))
        check_name = models.IndustryForm.objects.filter(name=name).count()
        if check_name > 0:
            raise ValidationError(_("نام انتخابی شما قبلاانتخاب شده است."))
        return name

    def clean_registration_number(self):
        data = self.cleaned_data["registration_number"]
        try:
            int(data)
        except ValueError:
            raise ValidationError(_('شماره ثبت باید یک عدد باشد.'))
        if len(str(data)) != 5:
            raise ValidationError(_("شماره ثبت باید 5 رقمی باشد."))
        return data

    def clean_date_of_foundation(self):
        data = self.cleaned_data["date_of_foundation"]
        try:
            int(data)
        except ValueError:
            raise ValidationError(_("سال تاسیس باید یک عدد باشد."))
        if len(str(data)) != 4:
            raise ValidationError(_("سال تاسیس باید 4 رقمی باشد."))
        return data

    def clean_research_field(self):
        data = self.cleaned_data["research_field"]
        return data

    def clean_industry_type(self):
        data = self.cleaned_data["industry_type"]
        return data

    def clean_industry_address(self):
        data = self.cleaned_data["industry_address"]
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        if not re.match(r'^([\d]+)$', data):
            raise ValidationError(_("شماره وارد شده معتبر نمی باشد."))
        return data

    def clean_email_address(self):
        email_address = self.cleaned_data.get('email_address')
        if self.user.email and self.user.email != email_address:
            raise ValidationError(_('ایمیل وارد شده با ایمیل شما مطالبفت ندارد.'))
        return email_address


class IndustryInfoForm(forms.ModelForm):
    # photo = forms.FileField(required=False)
    # name = forms.CharField()
    # registration_number = forms.TextInput()
    # date_of_foundation = forms.TextInput()
    # research_field = forms.TextInput()
    # industry_type_choices = (
    #     (0, 'خصوصی'),
    #     (1, 'دولتی'),
    # )
    # industry_type = forms.IntegerField(error_messages={
    #     'invalid': 'لطفا نوع شرکت را انتخاب کنید.',
    #     'required': 'لطفا نوع شرکت را انتخاب کنید.',
    # })
    # industry_address = forms.CharField()
    # phone_number = forms.TextInput()
    # email_address = forms.EmailField()
    # services_products = forms.CharField(widget=forms.Textarea, required=False)
    # awards_honors = forms.CharField(widget=forms.Textarea, required=False)
    # tax_declaration = forms.FileField(required=False)

    class Meta:
        model = models.IndustryForm
        fields = '__all__'
        # fields = ['photo', 'name', 'registration_number', 'date_of_foundation', 'research_field',
        #           'industry_type', 'industry_address', 'phone_number', 'services_products',
        #           'email_address', 'awards_honors', 'tax_declaration']
        error_messages = {'industry_type': {
            'required': 'لطفا نوع شرکت را انتخاب نمایید.',
            'invalid': 'لطفا نوع شرکت را انتخاب نمایید',
        }}

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_industry_type(self):
        industry_type = self.cleaned_data.get('industry_type')
        print('the type is ', industry_type)
        if industry_type != 0 and industry_type != 1:
            raise ValidationError(_('لطفا نوع شرکت را انتخاب نمایید.'))

    def clean_name(self):
        data = self.cleaned_data.get('name')
        if not data:
            raise ValidationError(_('لطفا نام شرکت را وارد کنید.'))
        return data

    def clean_registration_number(self):
        data = self.cleaned_data.get('registration_number')
        if not data:
            raise ValidationError(_("لطفا شماره ثبت را وارد کنید."))
        if data <= 0 or len(str(data)) != 5:
            raise ValidationError(_("شماره ثبت یک عدد پنج رقمی است."))
        return data

    def clean_date_of_foundation(self):
        data = self.cleaned_data.get('date_of_foundation')
        if not data:
            raise ValidationError(_('لطفا تاریخ تاسیس را وارد نمایید.'))
        if data <= 0 or len(str(data)) != 4:
            raise ValidationError(_('تاریخ تاسیس یک عدد چهار رقمی است.'))
        return data

    def clean_email_address(self):
        data = self.cleaned_data.get('email_address')
        if not data:
            raise ValidationError(_('لطفا ایمیل شرکت را وارد نمایید.'))
        if self.user.email and self.user.email != data:
            raise ValidationError(_("ایمیل وارد شده با ایمیل شما مطابقت ندارد."))
        return data

    def clean_industry_type(self):
        data = self.cleaned_data.get('industry_type')
        if data is None:
            raise ValidationError(_('لطفا نوع شرکت را انتخاب کنید.'))
        return data

    def clean_industry_address(self):
        data = self.cleaned_data.get('industry_address')
        if not data:
            raise ValidationError(_('لطفا نشانی را وارد نمایید.'))
        return data

    def clean_phone_number(self):
        data = self.cleaned_data.get('phone_number')
        if not re.match(r'^([+\d]+)$', data):
            raise ValidationError(_('لطفا شماره تلفن را به درستی وارد نمایید.'))
        return data

    def clean_research_field(self):
        data = self.cleaned_data.get('research_field')
        if not data:
            raise ValidationError(_('لطفا حوزه فعالیت را وارد نمایید.'))
        return data


class ProjectForm(forms.Form):
    key_words = forms.CharField(required=False)
    potential_problems = forms.CharField(required=False)
    project_title_persian = forms.CharField()
    project_title_english = forms.CharField()
    research_methodology_choice = (
        (0, 'کیفی'),
        (1, 'کمی'),
    )
    research_methodology = forms.IntegerField(widget=forms.RadioSelect(choices=research_methodology_choice),
                                              error_messages={'required': 'روش تحقیق را انتخاب نمایید'})
    main_problem_and_importance = forms.CharField()
    approach = forms.CharField(required=False)
    progress_profitability = forms.CharField()
    predict_profit = forms.IntegerField()
    required_lab_equipment = forms.CharField()
    project_phase = forms.CharField()
    required_budget = forms.IntegerField()
    policy = forms.CharField()

    class Meta:
        fields = [
            'project_title_persian', 'project_title_english', 'key_words', 'research_methodology',
            'main_problem_and_importance', 'progress_profitability', 'required_lab_equipment',
            'predict_profit', 'approach', 'policy', 'project_phase', 'required_budget', 'required_technique',
            'potential_problems',
        ]

    def clean_project_title_persian(self):
        data = self.cleaned_data["project_title_persian"]
        for item in data:
            if 65 <= ord(item) <= 90:
                raise ValidationError(_("به فارسی تایپ شود لطفا"))
            if 97 <= ord(item) <= 122:
                raise ValidationError(_("به فارسی تایپ شود لطفا"))
        return data

    def clean_project_title_english(self):
        data = self.cleaned_data["project_title_english"]
        for item in data:
            if 1750 > ord(item) > 1560:
                raise ValidationError(_("به انگلیسی تایپ شود لطفا"))
        return data
