from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from . import models

from datetime import date

class InitailForm(forms.ModelForm):

    class Meta:
        model = models.ResearcherProfile
        fields =[
            'first_name' ,'last_name' ,'photo' ,'address' ,'national_code' ,'entry_year' ,'grade',
            'university' ,'major' ,'home_number' ,'phone_number' ,'email' ,'student_number',
        ]
        widgets = {
            'photo' : forms.FileInput(attrs={'id':"upload-input" ,'accept':"image/png, image/jpeg"}),
            'first_name' : forms.TextInput(attrs={'id':"FirstName" ,'class' : "w-100"}),
            'last_name'  : forms.TextInput(attrs={'id':"LastName" ,'class' : "w-100"}),
            'major'  : forms.TextInput(attrs={'id':"Field" ,'class' : "w-100"}),
            'national_code'  : forms.TextInput(attrs={'id':"nationalCode" ,'class' : "w-100"}),
            'student_number' : forms.TextInput(attrs={'id':"student-num" ,'class' : "w-100"}),
            'entry_year' : forms.TextInput(attrs={'id':"enter-date" ,'class' : "w-100"}),
            'university' : forms.TextInput(attrs={'id':"Uni" ,'class' : "w-100"}),
            'address' : forms.Textarea(attrs={'dir':"rtl" ,'rows':"5" ,'id' : 'Address',
                                                  'class' : "w-100"}),
            'phone_number' : forms.TextInput(attrs={'id':"PhoneNum" ,'class' : "w-100"}),
            'home_number' : forms.TextInput(attrs={'id':"HomeNum" ,'class' : "w-100"}),
            'email' : forms.EmailInput(attrs={'id':"Email" ,'class' : "w-100"}),
            'grade' : forms.Select(attrs={'id':'rank'}),
        }
    
    def clean_national_code(self):
        data = self.cleaned_data["national_code"]
        for item in data:
            if ord(item) < 48 or ord(item) > 57:
                print('فقط عدد وارد کنید.')
                raise ValidationError(_("فقط عدد وارد کنید."))
        if len(data) < 10 and len(data) != 0:
            print('تعداد اعداد وارد شده اشتباه است.')
            raise ValidationError(_("تعداد اعداد وارد شده اشتباه است."))
        return data
    
    def clean_student_number(self):
        data = self.cleaned_data["student_number"]
        for item in data:
            if ord(item) < 48 or ord(item) > 57:
                print('فقط عدد وارد کنید.')
                raise ValidationError(_("فقط عدد وارد کنید."))
        return data
        
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

            if data > (int(this_year)-621):
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
    