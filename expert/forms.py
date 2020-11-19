from django import forms
from django.core.exceptions import ValidationError

from .models import *
from .tools.tools import *

import re

USER_ID_PATTERN = re.compile("^[\w]+$")

def has_number(string):
    for ch in string:
        if ch in '0123456789':
            return True
    return False


def completely_numeric(string):
    try:
        int(string)
        return True
    except:
        return False


class InitialInfoForm(forms.ModelForm):
    userId = forms.CharField(max_length=150, required=False)
    class Meta:
        model = ExpertForm
        fields = ['photo', 'fullname', 'special_field', 'scientific_rank',
                  'university', 'home_number', 'phone_number']
        error_messages = {
            # 'photo'           : {'required': "عکس نمی تواند خالی باشد."} ,
            'fullname'        : {'required': "نام و نام خانوادگی نمی تواند خالی باشد."},
            'special_field'   : {'required': "حوزه تخصصی نمی تواند خالی باشد."},
            'scientific_rank' : {'required': 'مرتبه علمی نباید خالی باشد.'},
            'university'      : {'required': "دانشگاه مورد نظر نمی تواند خالی باشد."},
            # 'home_number'     : {'required': "شماره تلفن منزل نمی تواند خالی باشد."},
            'phone_number'    : {'required': "شماره تلفن همراه نمی تواند خالی باشد."},
        }
    # photo = forms.FileField(max_length=256, error_messages={'required': "عکس نمی تواند خالی باشد."})
    # fullname = forms.CharField(max_length=128, error_messages={'required': "نام و نام خانوادگی نمی تواند خالی باشد."})
    # special_field = forms.CharField(max_length=256, error_messages={'required': "حوزه تخصصی نمی تواند خالی باشد."})
    # national_code = forms.CharField(error_messages={'required': "کد ملی نمی تواند خالی باشد."})
    # scientific_rank = forms.IntegerField(error_messages={'required': 'مرتبه علمی نباید خالی باشد!'})
    # university = forms.CharField(max_length=128, error_messages={'required': "دانشگاه مورد نظر نمی تواند خالی باشد."})
    # home_number = forms.CharField(error_messages={'required': "شماره تلفن منزل نمی تواند خالی باشد."})
    # phone_number = forms.CharField(error_messages={'required': "شماره تلفن همراه نمی تواند خالی باشد."})
    # email_address = forms.EmailField(error_messages={'required': "ایمیل نمی تواند خالی باشد.",
    #                                                  'invalid': 'ایمیل وارد شده نامعتبر است.'})

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        if has_number(fullname):
            raise forms.ValidationError('نام نباید شامل عدد باشد.')
        return fullname

    def clean_userId(self):
        data = self.cleaned_data["userId"]
        if not bool(USER_ID_PATTERN.match(data)):
            raise ValidationError('فقط شامل حروف و اعداد و خط زیر است.')
        return data

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        try:
            int(phone_number)
        except ValueError:
            raise forms.ValidationError('شماره تلفن همراه باید یک عدد باشد.')

        if len(phone_number) != 11:
            raise forms.ValidationError('شماره تلفن همراه باید یازده رقمی باشد.')

        return phone_number


class ExpertInfoForm(forms.ModelForm):
    keywords = forms.CharField(required=False)
    userId = forms.CharField(max_length=150, required=False)

    class Meta:
        model = ExpertForm
        exclude = ['expert_user', 'photo','keywords', 'eq_test', 'lab_equipment']
        error_messages = {
            'userId': {
                'required': 'شناسه کاربری نمی تواند خالی باشد.'
            },
            'special_field': {
                'required': 'حوزه تخصصی نمی تواند خالی باشد.'
            },
            'scientific_rank': {
                'required': 'مرتبه علمی نمی تواند خالی باشد'
            },
            'phone_number':{
                "required": "شماره تلفن همراه نمی تواند خالی باشد."
            },
            # 'home_address': {
            #     'required': 'آدرس نمی تواند خالی باشد.'
            # },
        }

        widgets = {
            'home_address': forms.Textarea(attrs={'rows': "5",}),
        }

    def clean_userId(self):
        data = self.cleaned_data["userId"]
        if not bool(USER_ID_PATTERN.match(data)):
            raise ValidationError('فقط شامل حروف و اعداد و خط زیر است.')
        return data
    

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        if national_code is None:
            return national_code
            # raise forms.ValidationError("کد ملی نمی تواند خالی باشد.")
        try:
            int(national_code)
        except ValueError:
            raise forms.ValidationError('کد ملی باید یک عدد باشد.')

        if len(national_code) != 10:
            raise forms.ValidationError('کد ملی باید ده رقمی باشد.')

        return national_code

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        try:
            int(phone_number)
        except ValueError:
            raise forms.ValidationError('شماره تلفن همراه باید یک عدد باشد.')

        if len(phone_number) != 11:
            raise forms.ValidationError('شماره تلفن همراه باید یازده رقمی باشد.')

        return phone_number

    # def clean_home_number(self):
    #     home_number = self.cleaned_data.get('home_number')
    #     if home_number == "":
    #         return home_number
    #     try:
    #         int(home_number)
    #     except ValueError:
    #         raise forms.ValidationError('شماره تلفن منزل باید یک عدد باشد.')

    #     if len(home_number) != 11:
    #         raise forms.ValidationError('شماره تلفن منزل باید یازده رقمی باشد.')

    #     return home_number
    
    def clean_number_of_grants(self):
        data = self.cleaned_data["number_of_grants"]
        if data is not None:
            try:
                int(data)
            except:
                raise forms.ValidationError("تعداد گرنت ها باید به عدد باشد.")
        return data
    


class ScientificRecordForm(forms.ModelForm):
    class Meta:
        model = ScientificRecord
        fields = ['degree', 'major', 'university', 'city', 'date_of_graduation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['degree'].required = False
        self.fields['major'].required = False
        self.fields['university'].required = False
        self.fields['city'].required = False
        self.fields['date_of_graduation'].required = False

    def clean_date_of_graduation(self):
        year = self.cleaned_data.get('date_of_graduation')
        if year == "" :
            raise forms.ValidationError("سال اخذ مدرک باید خالی باشد.")
        try:
            int(year)
        except ValueError:
            raise forms.ValidationError('سال اخذ مدرک باید عدد باشد.')
        if int(year) < 1000 or int(year) > 9999:
            raise forms.ValidationError('سال اخذ مدرک باید چهار رقمی باشد.')
        return year

    def clean_degree(self):
        degree = self.cleaned_data.get('degree')
        if degree == "":
            raise forms.ValidationError('مقطع تحصیلی نمی تواند خالی باشد')
        if completely_numeric(degree):
            raise forms.ValidationError('مقطع تحصیلی نمی تواند عدد باشد')
        return degree

    def clean_major(self):
        major = self.cleaned_data.get('major')
        if major == "":
            raise forms.ValidationError('رشته تحصیلی نمی تواند خالی باشد')
        if completely_numeric(major):
            raise forms.ValidationError('رشته تحصیلی نمی تواند عدد باشد')
        return major

    def clean_university(self):
        university = self.cleaned_data.get('university')
        if university == "":
           raise forms.ValidationError('دانشگاه نمی تواند خالی باشد')
        if completely_numeric(university):
            raise forms.ValidationError('دانشگاه نمی تواند عدد باشد')
        return university

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city == "":
            raise forms.ValidationError('شهر نمی تواند خالی باشد')
        if completely_numeric(city):
            raise forms.ValidationError('شهر نمی تواند عدد باشد')
        return city


class ExecutiveRecordForm(forms.ModelForm):
    class Meta:
        model = ExecutiveRecord
        exclude = ['expert_form']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executive_post'].required = False
        self.fields['date_start_post'].required = False
        self.fields['date_end_post'].required = False
        self.fields['organization'].required = False
        self.fields['city'].required = False

    def clean_executive_post(self):
        executive_post = self.cleaned_data.get('executive_post')
        if executive_post == "":
            raise forms.ValidationError("سمت نمی تواند خالی باشد.")
        if completely_numeric(executive_post):
            raise forms.ValidationError('سمت نمی تواند عدد باشد')
        return executive_post

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city == "":
            raise forms.ValidationError("شهر نمی تواند خالی باشد.")
        if completely_numeric(city):
            raise forms.ValidationError('شهر نمی تواند عدد باشد')
        return city

    def clean_organization(self):
        organization = self.cleaned_data.get('organization')
        if organization == "":
            raise forms.ValidationError("محل خدمت نمی تواند خالی باشد.")
        if completely_numeric(organization):
            raise forms.ValidationError('محل خدمت نمی تواند عدد باشد')
        return organization

    def clean_date_start_post(self):
        start = self.cleaned_data.get('date_start_post')
        if start == "":
            raise forms.ValidationError("سال ورود نمی تواند خالی باشد.")
        try:
            int(start)
        except ValueError:
            raise forms.ValidationError('لطفا عدد چهار رقمی وارد کنید.')
        if len(start) != 4:
            raise forms.ValidationError('سال ورود باید چهار رقمی باشد.')
        return start

    def clean_date_end_post(self):
        end = self.cleaned_data.get('date_end_post')
        if end == "":
            raise forms.ValidationError("سال پایان نمی تواند خالی باشد.")
        try:
            int(end)
        except ValueError:
            raise forms.ValidationError('لطفا عدد چهار رقمی وارد کنید.')
        if len(end) != 4:
            raise forms.ValidationError('تاریخ پایان باید چهار رقمی باشد.')
        return end


class ResearchRecordForm(forms.ModelForm):
    class Meta:
        model = ResearchRecord
        exclude = ['expert_form']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['research_title'].required = False
        self.fields['researcher'].required = False
        self.fields['liable'].required = False

    def clean_research_title(self):
        title = self.cleaned_data.get('research_title')
        if title == "":
            raise forms.ValidationError('عنوان طرح نمی تواند خالی باشد')
        if completely_numeric(title):            
            raise forms.ValidationError('عنوان طرح نمی تواند عدد باشد')
        return title

    def clean_researcher(self):
        researcher = self.cleaned_data.get('researcher')
        if researcher == "":
            raise forms.ValidationError("نام مجری نمی تواند خالی باشد")
        if has_number(researcher):
            raise forms.ValidationError('نام مجری نمی تواند عدد باشد')
        return researcher

    def clean_liable(self):
        liable = self.cleaned_data.get('liable')
        if liable == "":
            raise forms.ValidationError('نام همکار نمی تواند خالی باشد')
        if has_number(liable):
            raise forms.ValidationError('نام همکار نمی تواند عدد باشد')
        return liable


class PaperRecordForm(forms.ModelForm):
    class Meta:
        model = PaperRecord
        exclude = ['expert_form']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['citation'].required = False
        self.fields['research_title'].required = False
        self.fields['date_published'].required = False
        self.fields['published_at'].required = False
        self.fields['impact_factor'].required = False

    def clean_citation(self):
        citation = self.cleaned_data.get('citation')
        if citation == "":
            raise forms.ValidationError('تعداد ارجاع نمی تواند خالی باشد')
        try:
            int(citation)
        except ValueError:
            raise forms.ValidationError('تعداد ارجاع باید عدد باشد.')

        return citation

    def clean_research_title(self):
        title = self.cleaned_data.get('research_title')
        if title == "":
            raise forms.ValidationError('عنوان مقاله نمی تواند خالی باشد')
        if completely_numeric(title):
            raise forms.ValidationError('عنوان مقاله نمی تواند عدد باشد')
        return title

    def clean_date_published(self):
        date_published = self.cleaned_data.get('date_published')
        if date_published == "":
            raise forms.ValidationError('تاریخ انتشار نمی تواند خالی باشد')
        try:
            int(date_published)
        except ValueError:
            raise forms.ValidationError('لطفا عدد چهار رقمی وارد کنید.')
        if len(date_published) != 4:
            raise forms.ValidationError('تاریخ انتشار باید چهار رقمی باشد.')
        return date_published

    def clean_published_at(self):
        published_at = self.cleaned_data.get('published_at')
        if published_at == "":
            raise forms.ValidationError('عنوان مقاله نمی تواند خالی باشد')
        if completely_numeric(published_at):
            raise forms.ValidationError('عنوان مقاله نمی تواند عدد باشد')
        return published_at

    def clean_impact_factor(self):
        impact_factor = self.cleaned_data.get('impact_factor')
        if impact_factor == None:
            raise forms.ValidationError('فاکتور تاثیرگذاری نمی تواند خالی باشد.')
        try:
            int(impact_factor)
        except ValueError:
            raise forms.ValidationError('فاکتور تاثیرگذاری باید عدد باشد.')

        return impact_factor


class ResearchQuestionForm(forms.ModelForm):
    class Meta:
        model = ResearchQuestion
        exclude = ['expert', 'submitted_date', 'status', 'uniqe_id']
        error_messages = {
            'question_title': {
                'required': 'لطفا عنوان سوال را وارد نمایید.'
            },
            'question_text': {
                'required': 'لطفا توضیحات سوال را وارد نمایید.'
            },
        }

    def clean_question_title(self):
        question_title = self.cleaned_data.get('question_title')
        if completely_numeric(question_title):
            raise forms.ValidationError('عنوان نمی تواند عدد باشد.')
        return question_title

    def clean_question_text(self):
        question_text = self.cleaned_data.get('question_text')
        if completely_numeric(question_text):
            raise forms.ValidationError('توضیحات نمی تواند تنها عدد باشد.')
        return question_text

    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachemnt')
        return attachment

class CommentForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea ,empty_value="None")
    attachment = forms.FileField(required=False)

    def clean_description(self):
        data = self.cleaned_data["description"]
        if data == "None":
            raise ValidationError("نظر خود را لطفا بنوبسید.")
        return data
    
    def clean_attachment(self):
        data = self.cleaned_data["attachment"]
        return data

class RequestResearcherForm(forms.ModelForm):
    # least_hour       = forms.IntegerField(required=False)
    # researcher_count = forms.IntegerField(required=False)
    expiration_date    = forms.CharField(max_length=50, required=False)

    class Meta:
        model = RequestResearcher
        fields = ['least_hour', 'researcher_count',]
    
    def clean_least_hour(self):
        data = self.cleaned_data["least_hour"]
        if data is "":
            raise ValidationError('حداقل ساعت نمی تواند خالی باشد.')
        if data < 1:
            raise ValidationError("مقدار حداقل ساعت وارد شده نامعتر می باشد.")
        return data
    
    def clean_researcher_count(self):
        data = self.cleaned_data["researcher_count"]
        if data is "":
            raise ValidationError('تعداد دانشجو نمی تواند خالی باشد.')
        if data < 1:
            raise ValidationError("تعداد دانشجو وارد شده نامعتر می باشد.")
        return data

    def clean_expiration_date(self):
        data = self.cleaned_data["expiration_date"]
        if data is "":
            raise ValidationError('تاریخ اعتبار درخواست نمی تواند خالی باشد.')
        try:
            return JalaliToGregorianDate(data)
        except:
            raise ValidationError('تاریخ اعتبار درخواست معتبر نمی باشد.')
    