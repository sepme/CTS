from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from expert.forms import is_numeric
from . import models

from datetime import date

PER_ZERO = 1632
PER_NINE = 1641
ENG_ZERO = 48
ENG_NINE = 57


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
        for item in data:
            if ord(item) < ENG_ZERO or ord(item) > ENG_NINE:
                if ord(item) < PER_ZERO or ord(item) > PER_NINE:
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
                  'email', 'team_work', 'creative_thinking', 'interest_in_major', 'motivation',
                  'sacrifice', 'diligence', 'interest_in_learn', 'punctuality', 'data_collection',
                  'project_knowledge', 'description', 'photo',
                  ]

    def clean_photo(self):
        data = self.cleaned_data["photo"]
        return data

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        print('firt_name ,', data)
        return data

    def clean_last_name(self):
        data = self.cleaned_data["last_name"]
        print('last_name ,', data)
        return data

    def clean_major(self):
        major = self.cleaned_data.get('major')
        print('major ,', major)
        return major

    def clean_national_code(self):
        data = self.cleaned_data["national_code"]
        for item in data:
            if ord(item) < ENG_ZERO or ord(item) > ENG_NINE:
                if ord(item) < PER_ZERO or ord(item) > PER_NINE:
                    raise ValidationError(_("فقط عدد وارد کنید."))

        if len(data) < 10 and len(data) != 0:
            print('تعداد اعداد وارد شده اشتباه است.')
            raise ValidationError(_("تعداد اعداد وارد شده اشتباه است."))
        print('national_code ,', data)
        return data

    def clean_grade(self):
        data = self.cleaned_data["grade"]
        print('grade ,', data)
        return data

    def clean_university(self):
        data = self.cleaned_data["university"]
        print('university ,', data)
        return data

    def clean_entry_year(self):
        data = self.cleaned_data["entry_year"]
        if data:
            this_year = str(date.today().year)

        if data > (int(this_year) - 621):
            print("سال را اشتباه وارد کرده اید.")
            raise ValidationError(_("سال را اشتباه وارد کرده اید."))
        print('entry_year ,', data)
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        print('email ,', data)
        return data

    def clean_address(self):
        data = self.cleaned_data["address"]
        print('address ,', data)
        return data

    def clean_student_number(self):
        data = self.cleaned_data["student_number"]
        for item in data:
            if ord(item) < ENG_ZERO or ord(item) > ENG_NINE:
                if ord(item) < PER_ZERO or ord(item) > PER_NINE:
                    raise ValidationError(_("فقط عدد وارد کنید."))
        print('student_number ,', data)
        return data

    def clean_home_number(self):
        data = self.cleaned_data["home_number"]
        for item in data:
            if ord(item) < ENG_ZERO or ord(item) > ENG_NINE:
                if ord(item) < PER_ZERO or ord(item) > PER_NINE:
                    print("فقط عدد وارد کنید.")
                    raise ValidationError(_("فقط عدد وارد کنید."))
        print('entry_year ,', data)
        return data

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        for item in data:
            if ord(item) < ENG_ZERO or ord(item) > ENG_NINE:
                if ord(item) < PER_ZERO or ord(item) > PER_NINE:
                    print("فقط عدد وارد کنید.")
                    raise ValidationError(_("فقط عدد وارد کنید."))
        print('phone_number ', data)
        return data

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
            'email': {'required': 'پست الکترونیکی نمی تواند خالی باشد.',
                      'invalid': 'پست الکترونیکی وارد شده نامعتبر است.'},

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

    def clean_email(self):
        current_email = self.cleaned_data.get('email')
        email = models.ResearcherProfile.objects.filter(email=current_email)
        if email.exists():
            raise forms.ValidationError('کاربر با این ایمیل قبلا ثبت نام شده است')

        return current_email

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        print('mellicode:', national_code)
        try:
            int(national_code)
        except ValueError:
            raise forms.ValidationError('کد ملی باید یک عدد باشد.')

        if len(national_code) != 10:
            raise forms.ValidationError('کد ملی باید ده رقمی باشد.')

        return national_code

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
        return entry_year
