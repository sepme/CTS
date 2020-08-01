from django import forms
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from . import models


class RandDBasicInfoForm(forms.ModelForm):

    class Meta:
        model = models.RandDProfile
        fields = ('photo', 'RandDname', 'registration_number', 'date_of_foundation',
                  'research_field', 'RandD_type', 'phone_number')
        
        # error_messages = {
        #     'photo'               : { 'required' : 'عکس نمی تواند خالی باشد.'}, 
        #     'RandDname'                : { 'required' : 'نام نمی تواند خالی باشد.'},
        #     'registration_number' : { 'required' : 'شماره ثبت نمی تواند خالی باشد.'},
        #     'date_of_foundation'  : { 'required' : 'شماره تاسیس نمی تواند خالی باشد.'},
        #     'research_field'      : { 'required' : 'حوزه فعالیت را وارد کنید.'},
        #     'industry_type'       : { 'required' : 'نوع شرکت نمی تواند خالی باشد.'},
        #     'phone_number'        : { 'required' : 'تلفن نمی تواند خالی باشد.'},
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['RandDname'].required = False
        self.fields['photo'].required = False
        self.fields['registration_number'].required = False
        self.fields['date_of_foundation'].required = False
        self.fields['research_field'].required = False
        self.fields['RandD_type'].required = False
        self.fields['phone_number'].required = False


    # def clean_photo(self):
    #     data = self.cleaned_data["photo"]
    #     if data is None:
    #         raise ValidationError(_("عکس نمی تواند خالی باشد."))
    #     return data

    def clean_RandDname(self):
        RandDname = self.cleaned_data.get('RandDname')
        if RandDname is None or RandDname == '':
            raise ValidationError(_("نام نمی تواند خالی باشد."))
        check_RandDname = models.RandDProfile.objects.filter(RandDname=RandDname).count()
        if check_RandDname > 0:
            raise ValidationError(_("نام انتخابی شما قبلاانتخاب شده است."))
        return RandDname

    def clean_registration_number(self):
        data = self.cleaned_data["registration_number"]
        if data is "":
            raise ValidationError(_("شماره ثبت نمی تواند خالی باشد."))
        try:
            int(data)
        except ValueError:
            raise ValidationError(_('شماره ثبت باید یک عدد باشد.'))
        if len(str(data)) != 5:
            raise ValidationError(_("شماره ثبت باید 5 رقمی باشد."))
        return data

    def clean_date_of_foundation(self):
        data = self.cleaned_data["date_of_foundation"]
        if data is "":
            raise ValidationError(_("سال تاسیس نمی تواند خالی باشد."))
        try:
            int(data)
        except ValueError:
            raise ValidationError(_("سال تاسیس باید یک عدد باشد."))
        if len(str(data)) != 4:
            raise ValidationError(_("سال تاسیس باید 4 رقمی باشد."))
        return data

    def clean_research_field(self):
        data = self.cleaned_data["research_field"]
        if data == "":
            raise ValidationError(_("حوزه فعالیت نمی تواند خالی باشد."))
        return data

    def clean_RandD_type(self):
        data = self.cleaned_data["RandD_type"]                
        if data == "":
            raise ValidationError(_("نوع شرکت نمی تواند خالی باشد."))
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        if data == "":
            raise ValidationError(_('تلفن نمی تواند خالی باشد.'))
        try:
            int(data)
        except ValueError:
            raise ValidationError(_("شماره وارد شده معتبر نمی باشد."))
        if len(data) != 11:
            raise forms.ValidationError('شماره تلفن همراه باید یازده رقمی باشد.')
        return data

class RandDInfoForm(forms.ModelForm):

    class Meta:
        model = models.RandDProfile
        fields = ('photo', 'RandDname', 'registration_number', 'date_of_foundation',
                  'research_field', 'RandD_type', 'address', 'phone_number',
                  'tax_declaration', 'services_products', 'awards_honors')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['RandDname'].required  = False
        self.fields['photo'].required = False
        self.fields['registration_number'].required = False
        self.fields['date_of_foundation'].required  = False
        self.fields['research_field'].required      = False
        self.fields['RandD_type'].required          = False
        self.fields['address'].required             = False
        self.fields['tax_declaration'].required     = False
        self.fields['services_products'].required   = False
        self.fields['awards_honors'].required       = False 


class ResearchGroupInfoForm(forms.ModelForm):

    class Meta:
        model = models.ResearchGroupProfile
        exclude = ['industry_user', 'interfacePerson', "userId"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = False




class ResearchGroupBasicInfoForm(forms.ModelForm):

    class Meta:
        model = models.ResearchGroupProfile
        exclude = ['industry_user', 'interfacePerson', 'address']

        error_messages = {
            'name'       : {'required' : "نام نمی تواند خالی باشد."},
            'photo'      : {'required' : "عکس نمی تواند خالی باشد."},
            'type_group' : {'required' : "نوع شرکت نمی تواند خالی باشد."},
            'subordinateResearch' : {'required' : "نام پژوهشکده تابعه نمی تواند خالی باشد."},
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['photo'].required = False
        self.fields['type_group'].required = False
        self.fields['subordinateResearch'].required = False

    def clean_name(self):
        data = self.cleaned_data["name"]
        if data == "":
            raise ValidationError("نام نمی تواند خالی باشد.")
        return data
    
    # def clean_photo(self):
    #     data = self.cleaned_data["photo"]
    #     if data is None:
    #         raise ValidationError("عکس نمی تواند خالی باشد.")
    #     return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        if data == "":
            raise ValidationError("شماره تلفن نمی تواند خالی باشد.")
        return data
    

    def clean_type_group(self):
        data = self.cleaned_data["type_group"]
        if data == "":
            raise ValidationError("نوع شرکت نمی تواند خالی باشد.")
        return data
    
    def clean_subordinateResearch(self):
        data = self.cleaned_data["subordinateResearch"]
        if data == "":
            raise ValidationError("نام پژوهشکده تابعه نمی تواند خالی باشد.")
        return data

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
    potential_problems = forms.CharField(required=False ,widget=forms.Textarea)
    project_title_persian = forms.CharField()
    project_title_english = forms.CharField()
    research_methodology_choice = (
        (0, 'کیفی'),
        (1, 'کمی'),
    )
    research_methodology = forms.IntegerField(widget=forms.RadioSelect(choices=research_methodology_choice),
                                              error_messages={'required': 'روش تحقیق را انتخاب نمایید'})
    main_problem_and_importance = forms.CharField(widget=forms.Textarea)
    approach = forms.CharField(required=False ,widget=forms.Textarea)
    progress_profitability = forms.CharField(widget=forms.Textarea)
    predict_profit = forms.IntegerField()
    required_lab_equipment = forms.CharField(widget=forms.Textarea)
    required_method = forms.CharField(widget=forms.Textarea)
    project_phase = forms.CharField(widget=forms.Textarea)
    required_budget = forms.IntegerField()
    policy = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = [
            'project_title_persian', 'project_title_english', 'key_words', 'research_methodology',
            'main_problem_and_importance', 'progress_profitability', 'required_lab_equipment',
            'predict_profit', 'approach', 'policy', 'project_phase', 'required_budget', 'required_method',
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

    def clean_required_method(self):
        data = self.cleaned_data["required_method"]

        return data

    def clean_predict_profit(self):
        data = self.cleaned_data["predict_profit"]
        # if not data & (1 << 47):
            # raise ValidationError(_("مقدار وارد شده بیش از حد مجاز است."))
        return data
    
    def clean_required_budget(self):
        data = self.cleaned_data["required_budget"]
        # if not data & (1 << 47):
            # raise ValidationError(_("مقدار وارد شده بیش از حد مجاز است."))
        return data
    
    
class CommentForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea ,empty_value="None")
    attachment = forms.FileField(required=False)

    def clean_description(self):
        data = self.cleaned_data["description"]
        if data == "None":
            raise ValidationError(_("نظر خود را لطفا بنوبسید."))
        return data
    
    def clean_attachment(self):
        data = self.cleaned_data["attachment"]
        return data

class basicInterfacePersonForm(forms.ModelForm):
    industry_type = forms.CharField(max_length=15, required=False)

    class Meta:
        model = models.InterfacePerson
        exclude = ['']

        # error_messages = {
        #     'fullname'     : {'required' : 'نام و نام خانوادگی نمی تواند خالی باشد.'},
        #     'position'     : {'required' : 'سمت نمی تواند خالی باشد.'},
        #     'phone_number' : {'required' : 'شماره همراه نمی تواند خالی باشد.'},
        #     'email'        : {'required' : "پست الکترونیکی نمی تواند خالی باشد."} ,
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fullname'].required     = False
        self.fields['position'].required     = False
        self.fields['phone_number'].required = False
        self.fields['email'].required        = False

    def clean_fullname(self):
        data = self.cleaned_data["fullname"]
        if data == "":
            raise ValidationError("نام و نام خانوادگی نمی تواند خالی باشد.")
        return data
    
    def clean_industry_type(self):
        data = self.cleaned_data["industry_type"]
        if data == "":
            raise ValidationError("نوع شرکت نمی تواند خالی باشد.")
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        if data == "":
            raise ValidationError(_('تلفن نمی تواند خالی باشد.'))
        try:
            int(data)
        except ValueError:
            raise ValidationError(_("شماره وارد شده معتبر نمی باشد."))
        if len(data) != 11:
            raise forms.ValidationError('شماره تلفن همراه باید یازده رقمی باشد.')
        return data

    def clean_position(self):
        data = self.cleaned_data["position"]
        if data == "":
            raise ValidationError("سمت نمی تواند خالی باشد.")
        return data
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        if data == "":
            raise ValidationError("پست الکترونیکی نمی تواند خالی باشد.")
        return data
    

class interfacePersonForm(forms.ModelForm):
    class Meta:
        model = models.InterfacePerson
        exclude = ['']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fullname'].required     = False
        self.fields['position'].required     = False
        self.fields['phone_number'].required = False
        self.fields['email'].required        = False

    def clean_fullname(self):
        data = self.cleaned_data["fullname"]
        if data == "":
            raise ValidationError("نام و نام خانوادگی نمی تواند خالی باشد.")
        return data
    
    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        if data == "":
            raise ValidationError(_('تلفن نمی تواند خالی باشد.'))
        try:
            int(data)
        except ValueError:
            raise ValidationError(_("شماره وارد شده معتبر نمی باشد."))
        if len(data) != 11:
            raise forms.ValidationError('شماره تلفن همراه باید یازده رقمی باشد.')
        return data

    def clean_position(self):
        data = self.cleaned_data["position"]
        if data == "":
            raise ValidationError("سمت نمی تواند خالی باشد.")
        return data
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        if data == "":
            raise ValidationError("پست الکترونیکی نمی تواند خالی باشد.")
        return data
    