from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from expert.forms import is_numeric
from . import models,views

from datetime import date

def is_numeric(string):
    for ch in string:
        if ch in '0123456789':
            return True
    return False

def completely_numeric(string):
    check = True
    for ch in string:
        if ch in '0123456789':
            check = False
    return check


class InitailForm(forms.ModelForm):
    class Meta:
        model = models.ResearcherProfile
        fields = [
            'first_name', 'last_name', 'photo', 'address', 'national_code', 'entry_year', 'grade',
            'university', 'major', 'home_number', 'phone_number', 'email', 'student_number'
        ]
        widgets = {
            'photo': forms.FileInput(attrs={'id': "upload-input", 'accept': "image/png, image/jpeg"}),
            'first_name': forms.TextInput(attrs={'id': "FirstName", 'class': "w-100"}),
            'last_name': forms.TextInput(attrs={'id': "LastName", 'class': "w-100"}),
            'major': forms.TextInput(attrs={'id': "Field", 'class': "w-100"}),
            'national_code': forms.TextInput(attrs={'id': "nationalCode", 'class': "w-100"}),
            'student_number': forms.TextInput(attrs={'id': "student-num", 'class': "w-100"}),
            'entry_year': forms.TextInput(attrs={'id': "enter-date", 'class': "w-100"}),
            'university': forms.TextInput(attrs={'id': "Uni", 'class': "w-100"}),
            'address': forms.Textarea(attrs={'dir': "rtl", 'rows': "5", 'id': 'Address',
                                             'class': "w-100"}),
            'phone_number': forms.TextInput(attrs={'id': "PhoneNum", 'class': "w-100"}),
            'home_number': forms.TextInput(attrs={'id': "HomeNum", 'class': "w-100"}),
            'email': forms.EmailInput(attrs={'id': "Email", 'class': "w-100"}),
            'grade': forms.Select(attrs={'id': 'rank'}),
        }

    def clean_national_code(self):
        data = self.cleaned_data["national_code"]
        try:
            int(data)
        except:
            raise ValidationError(_("فقط عدد وارد کنید."))
        if len(data) < 10 and len(data) != 0:
            print('تعداد اعداد وارد شده اشتباه است.')
            raise ValidationError(_("تعداد اعداد وارد شده اشتباه است."))
        return data

    # def clean_student_number(self):
    #     data = self.cleaned_data["student_number"]
    #     for item in data:
    #         if ord(item) < 48 or ord(item) > 57:
    #             print('فقط عدد وارد کنید.')
    #             raise ValidationError(_("فقط عدد وارد کنید."))
    #     return data

    def clean_home_number(self):
        data = self.cleaned_data["home_number"]
        for item in data:
            if ord(item) < 48 or ord(item) > 57:
                raise ValidationError(_("فقط عدد وارد کنید."))
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        for item in data:
            if ord(item) < 48 or ord(item) > 57:
                raise ValidationError(_("فقط عدد وارد کنید."))
        return data

    def clean_entry_year(self):
        data = self.cleaned_data["entry_year"]
        if data:
            this_year = str(date.today().year)

            if data > (int(this_year) - 621):
                raise ValidationError(_("سال را اشتباه وارد کرده اید."))

        return data

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        return photo

    def clean_address(self):
        data = self.cleaned_data["address"]
        return data

    def clean_grade(self):
        data = self.cleaned_data["grade"]
        return data

    def clean_university(self):
        university = self.cleaned_data.get('university')
        return university

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name

    def clean_last_name(self):
        data = self.cleaned_data["last_name"]
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        return data

    def clean_major(self):
        data = self.cleaned_data["major"]
        return data


class ResearcherProfileForm(forms.ModelForm):
    class Meta:
        model = models.ResearcherProfile
        fields = ['first_name', 'last_name', 'major', 'national_code', 'grade', 'university',
                  'entry_year', 'student_number', 'address', 'home_number', 'phone_number',
                  'team_work', 'creative_thinking', 'interest_in_major', 'motivation',
                  'diligence', 'interest_in_learn', 'punctuality', 'data_collection',
                  'project_knowledge', 'description', 'photo','sacrifice','email',
                  ]
        # error_messages= {}

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_photo(self):
        data = self.cleaned_data["photo"]
        print("photo : " ,data)
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
    
        return email

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data

    def clean_last_name(self):
        data = self.cleaned_data["last_name"]
        return data

    def clean_major(self):
        major = self.cleaned_data.get('major')
        return major

    def clean_national_code(self):
        data = self.cleaned_data["national_code"]
        return data

    def clean_grade(self):
        data = self.cleaned_data["grade"]
        print('grade : ',data)
        return data

    def clean_university(self):
        data = self.cleaned_data["university"]
        return data

    def clean_entry_year(self):
        data = self.cleaned_data["entry_year"]
        if data:
            this_year = str(date.today().year)

        if int(data) > (int(this_year) - 621):
            raise ValidationError(_("سال را اشتباه وارد کرده اید."))
        return data

    def clean_address(self):
        data = self.cleaned_data["address"]
        return data

    def clean_student_number(self):
        data = self.cleaned_data["student_number"]
        return data

    def clean_home_number(self):
        home_number = self.cleaned_data["home_number"]
        try:
            int(home_number)
        except ValueError:
            raise forms.ValidationError('شماره تلفن منزل باید یک عدد باشد.')

        if len(home_number) != 11:
            raise forms.ValidationError('شماره تلفن منزل باید یازده رقمی باشد.')

        return home_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        try:
            int(phone_number)
        except ValueError:
            raise forms.ValidationError('شماره تلفن همراه باید یک عدد باشد.')

        if len(phone_number) != 11:
            raise forms.ValidationError('شماره تلفن همراه باید یازده رقمی باشد.')
        return phone_number

    def clean_team_work(self):
        data = self.cleaned_data["team_work"]
        print('teamwork ', data)
        return data

    def clean_creative_thinking(self):
        data = self.cleaned_data["creative_thinking"]
        print('creative_thinking ', data)
        return data

    def clean_interest_in_major(self):
        data = self.cleaned_data["interest_in_major"]
        print('interest in major ', data)
        return data

    def clean_motivation(self):
        data = self.cleaned_data["motivation"]
        print('motivation ', data)
        return data

    def clean_sacrifice(self):
        data = self.cleaned_data["sacrifice"]
        print('sacrif ', data)
        return data

    def clean_diligence(self):
        data = self.cleaned_data["diligence"]
        print('diligence ', data)
        return data

    def clean_interest_in_learn(self):
        data = self.cleaned_data["interest_in_learn"]
        print('interest in learn ', data)
        return data

    def clean_punctuality(self):
        data = self.cleaned_data["punctuality"]
        print('punctuality ', data)
        return data

    def clean_data_collection(self):
        data = self.cleaned_data["data_collection"]
        print('data_collection ', data)
        return data

    def clean_project_knowledge(self):
        data = self.cleaned_data["project_knowledge"]
        print('project knowledge ', data)
        return data

    def clean_description(self):
        data = self.cleaned_data["description"]
        print('description ', data)
        return data


class InitialInfoForm(forms.ModelForm):
    class Meta:
        model = models.ResearcherProfile
        # exclude = ['birth_year', 'team_work', 'creative_thinking', 'interest_in_major',
        #            'motivation', 'sacrifice', 'diligence', 'interest_in_learn', 'punctuality', 'data_collection',
        #            'project_knowledge', 'description', 'researcher_user']
        fields = ['first_name', 'last_name', 'photo', 'major', 'national_code', 'grade', 'university',
                  'entry_year', 'address', 'home_number', 'phone_number', 'student_number']
        error_messages = {
            'first_name': {'required': "نام نمی تواند خالی باشد."},
            'last_name': {'required': "نام خانوادگی نمی تواند خالی باشد."},
            'major': {'required': "رشته تحصیلی نمی تواند خالی باشد."},
            'national_code': {'required': "کد ملی نمی تواند خالی باشد."},
            'student_number': {'required': "شماره دانشجویی نمی تواند خالی باشد."},
            'entry_year': {'required': "سال ورود نمی تواند خالی باشد."},
            'grade': {'required': 'مقطع تحصیلی نمی تواند خالی باشد'},
            'university': {'required': "دانشگاه نمی تواند خالی باشد."},
            'address': {'required': "آدرس نمی تواند خالی باشد."},
            'phone_number': {'required': "شماره تلفن همراه نمی تواند خالی باشد."},
            'home_number': {'required': "شماره تلفن منزل نمی تواند خالی باشد."},
            # 'email': {'required': 'پست الکترونیکی نمی تواند خالی باشد.',
            #           'invalid': 'پست الکترونیکی وارد شده نامعتبر است.'},

        }

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

    # def clean_email(self):
    #     current_email = self.cleaned_data.get('email')
    #     email = models.ResearcherProfile.objects.filter(email=current_email)
    #     if email.exists():
    #         raise forms.ValidationError('کاربر با این ایمیل قبلا ثبت نام شده است')

    #     return current_email

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')        
        try:
            int(national_code)
        except ValueError:
            raise forms.ValidationError('کد ملی باید یک عدد باشد.')

        if len(national_code) != 10:
            raise forms.ValidationError('کد ملی باید ده رقمی باشد.')

        return national_code

    def clean_home_number(self):
        home_number = self.cleaned_data.get('home_number')
        try:
            int(home_number)
        except ValueError:
            raise forms.ValidationError('شماره تلفن منزل باید یک عدد باشد.')

        if len(home_number) != 11:
            raise forms.ValidationError('شماره تلفن منزل باید یازده رقمی باشد.')

        return home_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        try:
            int(phone_number)
        except ValueError:
            raise forms.ValidationError('شماره تلفن همراه باید یک عدد باشد.')

        if len(phone_number) != 11:
            raise forms.ValidationError('شماره تلفن همراه باید یازده رقمی باشد.')

        return phone_number

    def clean_student_number(self):
        number = self.cleaned_data.get('student_number')
        try:
            int(number)
        except ValueError:
            raise forms.ValidationError('شماره دانشجویی باید یک عدد باشد.')

        if len(number) != 8:
            raise forms.ValidationError('شماره دانشجویی باید هشت رقمی باشد.')

        return number

    def clean_entry_year(self):
        entry_year = self.cleaned_data.get('entry_year')
        try:
            int(entry_year)
        except ValueError:
            raise forms.ValidationError('سال ورود باید یک عدد باشد.')
        this_year = str(date.today().year)
        if int(entry_year) > (int(this_year) - 621):
                raise ValidationError(_("سال را اشتباه وارد کرده اید."))
        return entry_year

class ScientificRecordForm(forms.ModelForm):
    class Meta:
        model = models.ScientificRecord
        fields=['grade' ,'major' ,'university' ,'place' ,'graduated_year']

        error_messages = {
            'grade': {'required': "مقطع تحصیلی نمی تواند خالی باشد."},
            'major': {'required': "رشته تحصیلی نمی تواند خالی باشد."},
            'university': {'required': "دانشگاه نمی تواند خالی باشد."},
            'place': {'required': "شهر محل تحصیل نمی تواند خالی باشد."},
            'graduated_year': {'required': "سال اخذ مدرک نمی تواند خالی باشد."},
            }

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if is_numeric(grade):
            raise ValidationError(_("مقطع تحصیلی نمی تواند شامل عدد باشد."))
        print('grade' ,grade)
        return grade

    def clean_major(self):
        data = self.cleaned_data["major"]
        if is_numeric(data):
            raise ValidationError(_("رشته تحصیلی نمی تواند شامل عدد باشد."))
        print('major' ,data)
        return data

    def clean_university(self):
        data = self.cleaned_data["university"]
        if is_numeric(data):
            raise ValidationError(_("دانشگاه نمی تواند شامل عدد باشد."))
        print('university' ,data)
        return data
    
    def clean_place(self):
        data = self.cleaned_data["place"]
        if is_numeric(data):
            raise ValidationError(_("شهر نمی تواند شامل عدد باشد."))
        print('place' ,data)
        return data
    
    def clean_graduated_year(self):
        data = self.cleaned_data["graduated_year"]
        print('year' ,data)
        if data:
            try :
                int(data)
            except:
                raise ValidationError(_("عدد چهار رقمی وارد کنید."))    
            this_year = str(date.today().year)

            if int(data) > (int(this_year) - 621):
                raise ValidationError(_("سال را اشتباه وارد کرده اید."))
            
            if (int(data)/1000) < 1:
                raise ValidationError(_("عدد چهار رقمی وارد کنید."))
        return data
    
class ExecutiveRecordForm(forms.ModelForm):
    class Meta:
        model = models.ExecutiveRecord
        fields = ['post' ,'start' ,'end' ,'place' ,'city']

        error_messages = {
            'post': {'required': "سمت نمی تواند خالی باشد."},
            'start': {'required': "تارخ شروع نمی تواند خالی باشد."},
            'end': {'required': "تارخ پایان نمی تواند خالی باشد."},
            'place': {'required': "محل خدمت نمی تواند خالی باشد."},
            'city': {'required': "شهر نمی تواند خالی باشد."},
            }
    
    def clean_post(self):
        data = self.cleaned_data["post"]
        if is_numeric(data):
            raise ValidationError(_("سمت نمی تواند شامل عدد باشد."))
        return data
    
    def clean_start(self):
        data = self.cleaned_data["start"]
        print('start : ' ,data)
        if data:
            try:
                int(data)
            except ValueError:
                raise forms.ValidationError('سال باید یک عدد باشد.')

            this_year = int(date.today().year)

            if int(data) > (this_year - 621):
                raise ValidationError(_("سال را اشتباه وارد کرده اید."))
            
            if (int(data)/1000) < 1:
                raise ValidationError(_("عدد چهار رقمی وارد کنید."))
        return data

    def clean_end(self):
        data = self.cleaned_data["end"]
        start = self.cleaned_data.get('start')
        if data:
            try:
                int(data)
            except ValueError:
                raise forms.ValidationError('سال باید یک عدد باشد.')
            if start:
                if data < start:
                    raise forms.ValidationError('ترتیب سال ها رعایت شود.')
            
            this_year = int(date.today().year)

            if int(data) > (this_year - 621):
                raise ValidationError(_("سال را اشتباه وارد کرده اید."))

            if (int(data)/1000) < 1:
                raise ValidationError(_("عدد چهار رقمی وارد کنید."))
        return data
    
    def clean_place(self):
        data = self.cleaned_data["place"]
        if is_numeric(data):
            raise ValidationError(_("محل خدمت نمی تواند شامل عدد باشد."))
        return data
    
    def clean_city(self):
        data = self.cleaned_data["city"]
        if is_numeric(data):
            raise ValidationError(_("شهر نمی تواند شامل عدد باشد."))
        return data

class StudiousRecordForm(forms.ModelForm):
    class Meta:
        model = models.StudiousRecord
        fields = ['title' ,'presenter' ,'responsible' ,'status']

        error_messages = {
        'title': {'required': "عنوان طرح پژوهشی نمی تواند خالی باشد."},
        'presenter': {'required': "نام مجری نمی تواند خالی باشد."},
        'responsible': {'required': "مسئول اجرا / همکار نمی تواند خالی باشد."},
        'status': {'required': "وضعیت طرح پژوهشی نمی تواند خالی باشد."},
        }

    def clean_title(self):
        data = self.cleaned_data["title"]
        if is_numeric(data):
            raise ValidationError(_("عنوان طرح پژوهشی نمی تواند شامل عدد باشد."))
        return data
    
    def clean_presenter(self):
        data = self.cleaned_data["presenter"]
        if is_numeric(data):
            raise ValidationError(_("مجری نمی تواند شامل عدد باشد."))
        return data
    
    def clean_responsible(self):
        data = self.cleaned_data["responsible"]
        if is_numeric(data):
            raise ValidationError(_("مسئول اجرا / همکار نمی تواند شامل عدد باشد."))
        return data
    
    def clean_status(self):
        data = self.cleaned_data["status"]
        
        return data

class TechniqueInstanceForm(forms.Form):
    technique = forms.CharField(max_length=100 ,empty_value='None')
    confirmation_method = forms.CharField(max_length=100 ,required=False)
    resume = forms.FileField(required=False)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TechniqueInstanceForm, self).__init__(*args, **kwargs)

    def clean_technique(self):
        data = self.cleaned_data["technique"]
        if data == 'None':
            raise  ValidationError("عنوان تکنیک نمی تواند خالی باشد.")
        if data not in views.TECHNIQUES:
            raise  ValidationError("عنوان تکنیک اشتباه وارد شده است.")        
        if models.TechniqueInstance.objects.filter(researcher=self.user.researcheruser).filter(technique__technique_title=data).count() != 0:
            raise ValidationError(_("این تکنیک قبلا ذخیره شده است."))
        return data
    
    def clean_confirmation_method(self):
        data = self.cleaned_data["confirmation_method"]
        print("method :" ,data)
        if data == "":
            raise ValidationError(_("یکی از راه ثبت را انتخاب کنید."))
        return data

    def clean_resume(self):
        data = self.cleaned_data["resume"]
        method = self.cleaned_data.get('confirmation_method')
        print("method in resume :" ,method)
        print('resume : ' ,data)
        if method == 'exam':
            return data
        elif method is None:
            return data
        elif data is None:
            raise ValidationError(_('فایل مربوطه را آپلود کنید.'))
        return data

class TechniqueReviewFrom(forms.Form):
    request_body = forms.CharField(max_length=1000 ,required=False)
    request_confirmation_method = forms.CharField(max_length=100 ,required=False)
    new_resume = forms.FileField(required=False)

    def clean_request_body(self):
        data = self.cleaned_data["request_body"]        
        if data == "":
            raise ValidationError(_("توضیحات نمی تواند خالی باشد."))
        return data

    def clean_request_confirmation_method(self):
        data = self.cleaned_data["request_confirmation_method"]
        if data == '':
            raise ValidationError(_("یکی از راه های ارتفا را انتخاب کنید."))
        return data

    def clean_new_resume(self):
        data = self.cleaned_data["new_resume"]
        method = self.cleaned_data.get('request_confirmation_method')
        print('method in resume :' ,method)
        if method == 'exam':
            return data
        if method == None:
            return data
        elif data is None:
            raise ValidationError(_('فایل مربوطه را آپلود کنید.'))
        return data