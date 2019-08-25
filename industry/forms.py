from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from . import models


class IndustryBasicInfoForm(forms.Form):
    photo = forms.FileField(required=False)
    name = forms.CharField(max_length=300, required=False)
    registration_number = forms.CharField(max_length=50, required=False)
    date_of_foundation = forms.CharField(max_length=50, required=False)
    research_field = forms.CharField(max_length=300, required=False)
    industry_type = forms.IntegerField(error_messages={'invalid': 'لطفا نوع شرکت را انتخاب کنید.'})
    industry_address = forms.CharField(max_length=3000)
    phone_number = forms.CharField(max_length=15)
    email_address = forms.EmailField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_photo(self):
        data = self.cleaned_data["photo"]
        if data and (data.width > 200 or data.height > 200):
            data.thumbnail((200, 200))
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
        print('industry_type is', data)
        return data

    def clean_industry_address(self):
        data = self.cleaned_data["industry_address"]
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        for ch in data:
            if ch not in '+0123456789':
                raise ValidationError(_("شماره وارد شده معتبر نمی باشد."))
        return data

    def clean_email_address(self):
        email_address = self.cleaned_data.get('email_address')
        print(self.user.email, ' ?= ', email_address)
        if self.user.email and self.user.email != email_address:
            raise ValidationError(_('ایمیل وارد شده با ایمیل شما مطالبفت ندارد.'))
        return email_address


class IndustryInfoForm(forms.ModelForm):
    class Meta:
        model = models.IndustryForm
        fields = ['photo', 'name', 'registration_number', 'date_of_foundation', 'research_field',
                  'industry_type', 'industry_address', 'phone_number', 'services_products',
                  'email_address', 'awards_honors', 'tax_declaration']
        widgets = {
            'photo': forms.FileInput(attrs={'id': "upload-input", 'accept': "image/png, image/jpeg"}),
            'name': forms.TextInput(attrs={'class': "w-100", 'id': 'firmName'}),
            'registration_number': forms.TextInput(attrs={'class': "w-100", 'id': 'registerNum'}),
            'date_of_foundation': forms.TextInput(attrs={'class': "w-100", 'id': 'establishmentDate'}),
            'research_field': forms.TextInput(attrs={'class': "w-100", 'id': 'Field'}),
            'industry_type': forms.Select(attrs={"id": 'rank', "dir": 'rtl'}),
            'industry_address': forms.Textarea(attrs={'rows': "3", 'class': "w-100", 'id': "Address", 'dir': 'rtl'}),
            'phone_number': forms.TextInput(attrs={'class': "w-100", 'id': "phoneNum"}),
            'email_address': forms.EmailInput(attrs={'class': "w-100", 'id': "Email"}),
            'services_products': forms.Textarea(attrs={"class": "w-100", "placeholder": "اینجا وارد کنید ...",
                                                       "dir": "rtl", "rows": "5", "style": "margin-top: 0"}),
            'awards_honors': forms.Textarea(attrs={"class": "w-100", "placeholder": "اینجا وارد کنید ...",
                                                   "dir": "rtl", "rows": "5", "style": "margin-top: 0"}),
            'tax_declaration': forms.FileInput(attrs={'name': 'declaration', 'class': 'attach-input'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.ProjectForm
        # 'key_words','required_technique' ,
        fields = [
            'project_title_persian', 'project_title_english', 'research_methodology',
            'main_problem_and_importance', 'progress_profitability', 'required_lab_equipment',
            'predict_profit', 'innovation', 'approach', 'policy', 'project_phase', 'required_budget'
        ]

        # widgets ={
        #     "project_title_persian" : forms.TextInput(attrs={'id':"persian_label" ,'class':"w-100",}),
        #     "project_title_english" : forms.TextInput(attrs={'id':"latin_label" ,'class':"w-100",}),
        #     "main_problem_and_importance" : forms.Textarea(attrs={'rows':"5" ,'dir':"rtl" ,'placeholder':"اینجا وارد کنید ...",
        #                                                     'style':"margin-top: 0",'class':"w-100",}),
        #     "progress_profitability" : forms.Textarea(attrs={'rows':"5" ,'dir':"rtl" ,'placeholder':"اینجا وارد کنید ...",
        #                                                     'style':"margin-top: 0",'class':"w-100",}),

        #     'approach' : forms.Textarea(attrs={'rows':"7" ,'dir':"rtl" ,'placeholder':"اینجا وارد کنید ...",
        #                                                     'style':"margin-top: 0",'class':"w-100",}),
        #     'innovation' : forms.Textarea(attrs={'rows':"7" ,'dir':"rtl" ,'placeholder':"اینجا وارد کنید ...",
        #                                                     'style':"margin-top: 0",'class':"w-100",}),

        #     'required_lab_equipment' : forms.Textarea(attrs={'rows':"4" ,'dir':"rtl" ,'placeholder':"اینجا وارد کنید ...",
        #                                                     'style':"margin-top: 0",'class':"w-100",}),
        #     'required_technique'  : forms.Textarea(attrs={'rows':"4" ,'dir':"rtl" ,'placeholder':"اینجا وارد کنید ...",
        #                                                     'style':"margin-top: 0",'class':"w-100",}),
        #     'project_phase' : forms.Textarea(attrs={'rows':"4" ,'dir':"rtl" ,'placeholder':"اینجا وارد کنید ...",
        #                                                     'style':"margin-top: 0",'class':"w-100",}),
        #     'required_budget' : forms.Textarea(attrs={'rows':"4" ,'dir':"rtl" ,'placeholder':"اینجا وارد کنید ...",
        #                                                     'style':"margin-top: 0",'class':"w-100",}),
        #     'policy' : forms.Textarea(attrs={'rows':"7" ,'dir':"rtl" ,'placeholder':"اینجا وارد کنید ...",
        #                                                     'style':"margin-top: 0",'class':"w-100",}),
        # }

    def clean_project_title_persian(self):
        data = self.cleaned_data["project_title_persian"]
        for item in data:
            if 65 <= ord(item) <= 90:
                print("به فارسی تایپ شود لطفا")
                print(item, ord(item))
                raise ValidationError(_("به فارسی تایپ شود لطفا"))
            if 97 <= ord(item) <= 122:
                print("به فارسی تایپ شود لطفا")
                print(item, ord(item))
                raise ValidationError(_("به فارسی تایپ شود لطفا"))
        return data

    def clean_project_title_english(self):
        data = self.cleaned_data["project_title_english"]
        for item in data:
            if 1750 > ord(item) > 1560:
                print("به انگلیسی تایپ شود لطفا")
                raise ValidationError(_("به انگلیسی تایپ شود لطفا"))
        return data

    # def clean_key_words(self):
    #     data = self.cleaned_data["key_words"]
    #     print("key_words - " ,data)
    #     return data

    def clean_main_problem_and_importance(self):
        data = self.cleaned_data["main_problem_and_importance"]
        print("main_problem_and_importance - ", data)
        return data

    def clean_research_methodology(self):
        data = self.cleaned_data["research_methodology"]
        print("research_methodology - ", data)
        return data

    def clean_progress_profitability(self):
        data = self.cleaned_data["progress_profitability"]
        print("progress_profitability - ", data)
        return data

    def clean_required_lab_equipment(self):
        data = self.cleaned_data["required_lab_equipment"]
        print("required_lab_equipment - ", data)
        return data

    def clean_innovation(self):
        data = self.cleaned_data["innovation"]
        print("innovation - ", data)
        return data

    def clean_approach(self):
        data = self.cleaned_data["approach"]

        return data

    # def clean_required_technique(self):
    #     data = self.cleaned_data["required_technique"]
    #     print("required_technq" ,data)
    #     return data

    def clean_policy(self):
        data = self.cleaned_data["policy"]
        print("policy - ", data)
        return data

    def clean_required_budget(self):
        data = self.cleaned_data["required_budget"]
        print("required_budget - ", data)
        return data

    def clean_project_phase(self):
        data = self.cleaned_data["project_phase"]
        print("project_phase - ", data)
        return data

    def clean_predict_profit(self):
        predict_profit = self.cleaned_data.get('predict_profit')

        return predict_profit
