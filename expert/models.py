from django.db import models
from django.contrib.auth.models import User

class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,verbose_name = "کاربر استاد")
    expert_form = models.OneToOneField(ExpertForm, on_delete=models.CASCADE ,verbose_name = "فرم استاد") 
    date_register = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ ثبت نام")
    expert_point = models.IntegerField(verbose_name = "امتیاز استاد")
    def __str__(self):
        return self.expert_form.expert_firstname+self.expert_form.expert_lastname

class ExpertForm(models.Model): 
    expert_firstname = models.CharField(max_length=None,verbose_name = "نام")
    expert_lastname = models.CharField(max_length=None,verbose_name = "نام خانوادگی")
    special_field = models.CharField(max_length=None,verbose_name = "حوزه تخصصی")
    national_code = models.IntegerField(verbose_name = "کد ملی")
    scientific_rank = models.CharField(max_length=None,verbose_name = "مرتبه عامی")#need choice
    university = models.CharField(max_length=None,verbose_name = "دانشگاه محل فعالیت")
    home_adress = models.CharField(max_length=None,verbose_name = "ادرس منزل")
    phone_number = models.IntegerField(verbose_name = "شماره منزل")
    mobile_phone =  models.IntegerField(verbose_name = "شماره تلفن همراه")
    email_adress = models.EmailField(max_length=254,verbose_name = "ایمیل")
    eq_tset = models.OneToOneField(EqTset, on_delete=models.CASCADE,verbose_name = "تست EQ")
    awards = models.CharField(max_length=None,verbose_name = "افتخارات")
    method_of_introduction = models.CharField(max_length=None,verbose_name = "طریقه اشنایی با چمران تیم")
    posetive_feature_chamt =  models.CharField(max_length=None,verbose_name = "ویژگی های مثبت چمران تیم")#check 
    lab_equipment = models.CharField(max_length=None,verbose_name = "امکانات پژوهشی")
    number_of_resercher = models.IntegerField(verbose_name = "دانشجو تحت نظارت")#need choices
    has_indusryial_researech = models.BooleanField(verbose_name = "همکاری با شرکت خارج دانشگاه")
    number_of_grants = models.IntegerField(verbose_name = "تعداد گرنت")
    technique =  models.ManyToManyField(researcher.Technique,verbose_name = "تکنیک")#ask
    languages = models.CharField(max_length=None,verbose_name = "تسلط بر زبان های خارجی")#need other class

class ScientificRecord(models.Model):
    degree = models.CharField(max_length=None,verbose_name = "مقطع تحصیلی")
    major = models.CharField(max_length=None,verbose_name = "رشته تحصیلی")
    university = models.CharField(max_length=None,verbose_name = "دانشگاه")
    city = models.CharField(max_length=None,verbose_name = "شهر")
    date_of_grauate = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "سال اخذ مدرک")
    expert_form =  models.ForeignKey(ExpertForm, on_delete=models.CASCADE,verbose_name = "فرم استاد")
    
class ExecutiveRecord(models.Model):
    executive_post = models.CharField(max_length=None,verbose_name = "سمت")
    date_start_post = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تلریخ شروع")
    date_end_post = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ پایان")
    city =  models.CharField(max_length=None,verbose_name = "شهر")
    organization =  models.CharField(max_length=None,verbose_name = "مجل خدمت")
    expert_form =  models.ForeignKey(ExpertForm, on_delete=models.CASCADE,verbose_name = "فرم استاد")

class ResearchRecord(models.Model):
    research_title = models.CharField(max_length=None,verbose_name = "عنوان طرح")
    researcher = models.CharField(max_length=None,verbose_name = "نام مجری")
    co_researcher = models.CharField(max_length=None,verbose_name = "همکار")
    status = models.CharField(max_length=None,verbose_name = "وضعیت")#need choice
    expert_form =  models.ForeignKey(ExpertForm, on_delete=models.CASCADE,verbose_name = "فرم استاد")

class PaperRecord(models.Model):
    research_title = models.CharField(max_length=None,verbose_name = "عنوان مقاله")
    date_published = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ انتشار")
    publised_at = models.CharField(max_length=None,verbose_name = "محل انتشار")
    impact_factor = models.FloatField(verbose_name = "impact factor")
    citation = models.IntegerField(verbose_name = "تعداد ارجاع")
    expert_form =  models.ForeignKey(ExpertForm, on_delete=models.CASCADE,verbose_name = "فرم استاد")
    
class EqTset(models.Model):
    team_work = models.IntegerField(verbose_name = "روحیه کار تیمی")#need choice
    innovation = models.IntegerField(verbose_name = "تفکر خلاقانه")#need choice
    devtion = models.IntegerField(verbose_name = "تعهد و ازخوگذشتگی")#need choice
    productive_research = models.IntegerField(verbose_name = "پژوهش محصولمحور")#need choice
    national_commitment = models.IntegerField(verbose_name = "تعهد ملی")#need choice
    collecting_information = models.IntegerField(verbose_name = "جمع اوری داده")#need choice
    business_thinking = models.IntegerField(verbose_name = "روحیه بیزینسی")#need choice
    risk_averse = models.IntegerField(verbose_name = "ریسک پذیری")#need choice

class ExpertProjectHistory(models.Model):
    project_title_english = models.CharField(max_length=None,verbose_name = "عنوان مقاله")
    key_words = models.CharField(max_length=None,verbose_name = "کلمات کلیدی")#ask
    project_priority_level = models.FloatField(verbose_name = "اولویت پروژه")
    project_start_date = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ شروع")
    project_end_date = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ پایان")
    STATUS_CHOICE = (
        ('completed' ,'completed'),
        ('stoped' ,'stoped'),
    )
    project_status = models.CharField(max_length=9 ,choices = STATUS_CHOICE ,verbose_name="وضعیت")
    project_point = models.FloatField(verbose_name='امتیاز')
    project_income = models.IntegerField(verbose_name= 'درآمد')
    project_involveTech = models.CharField(max_length=500 ,verbose_name='تکنیک ها')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE ,verbose_name = "استاد")
    def __str__(self):
        return "history of " + self.profile.name 
    
    
class IndustryEvaluateExpert(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE,verbose_name = "استاد")
    industry  = models.OneToOneField(industry.Industry, on_delete=models.CASCADE,verbose_name = "صنعت ارزیابی کننده")
    INT_CHOICE =(
            ( 0 , '0'),
            ( 1 , '1'),
            ( 2 , '2'),
            ( 3 , '3'),
            ( 4 , '4'),
            ( 5 , '5'),
    )
    
    BOOL_CHOICE=(
            (FALSE,"false"),
            (TRUE,"true"),
    )

    ontime_progress_report =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "گزارش به موقع")
    cotribution_to_industry = models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان همکاری با صنعت")
    corect_estimation = models.IntegerField(choices= INT_CHOICE ,verbose_name = "تخمین استاد از هزینه و مواد")
    ontime_deadline = models.IntegerField(choices= INT_CHOICE ,verbose_name = "زمتن بندی اجرا")
    fullfill_requirment = models.IntegerField(choices= INT_CHOICE ,verbose_name = "اجرا مفاد قرارداد")
    diciplined = models.IntegerField(choices= INT_CHOICE ,verbose_name = "تعهد کاری")
    comited_to_goals = models.IntegerField(choices= INT_CHOICE ,verbose_name = "تحقق اداف پروژه")
    quality = models.IntegerField(choices= INT_CHOICE ,verbose_name = "کیفیت عملکرد")
    total_satisfaction = models.IntegerField(choices= INT_CHOICE ,verbose_name = "رضایت کلی")
    continue_coperate = models.BooleanField(choices= BOOL_CHOICE,verbose_name = "ادامه همکاری با استاد")
    using_chamt = models.BooleanField(choices= BOOL_CHOICE,verbose_name = "ادامه همکاری با چمران تیم")
    has_inovation = models.BooleanField(choices= BOOL_CHOICE,verbose_name = "دارای طرح جدید")
    
    def avarage(self):
        sum = 0.0
        sum = self.ontime_progress_report + self.cotribution_to_industry + self.corect_estimation + self.ontime_deadline
        sum = sum + self.fullfill_requirment + self.comited_to_goals + self.total_satisfaction + self.quality + self.diciplined

        ava = float(sum / 8)
        return ava
    
class ResearcherEvaluateExpert(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE,verbose_name = "")
    researcher  = models.OneToOneField(researcher.Researcher, on_delete=models.CASCADE,verbose_name = "")
    INT_CHOICE =(
            ( 0 , '0'),
            ( 1 , '1'),
            ( 2 , '2'),
            ( 3 , '3'),
            ( 4 , '4'),
            ( 5 , '5'),
    )
    
    GAIN_CHOICE=(
            ( 1 , 'تجریه عملی'),
            ( 2 , 'استاد به عنوان معرف عمل کرده'),
            ( 3 , 'مشارکت در مقاله'),
            ( 4 , 'دریافت پیشنهاد کار'),
            ( 5 , 'از قبل انجام کار پول دریافت کردم'),
    )

    tech_enough_info =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "اطاعات لازم نحوه کارتکنیک ها")
    tech_required_info = models.IntegerField(choices= INT_CHOICE ,verbose_name = "صحت تکنیک های مورد نیاز")
    totoal_gain = models.IntegerField(choices= INT_CHOICE ,verbose_name = "افزایش یادگیری")
    scientific_level = models.IntegerField(choices= INT_CHOICE ,verbose_name = "سطح علمی استاد")
    availability = models.IntegerField(choices= INT_CHOICE ,verbose_name = "در دسترس بودن")
    planing = models.IntegerField(choices= INT_CHOICE ,verbose_name = "تناسب برنامه با زمان دانشجو")
    flexible_schedule = models.IntegerField(choices= INT_CHOICE ,verbose_name = "انعطاف برنامه استاد")
    formal_act = models.IntegerField(choices= INT_CHOICE ,verbose_name = "برخورد محترمانه")
    distribute_task = models.IntegerField(choices= INT_CHOICE ,verbose_name = "به کارگیری متعادل دانشجویان")
    total_satisfaction = models.IntegerField(choices= INT_CHOICE ,verbose_name = "رضایت کلی")
    chamt_satisfaction = models.IntegerField(choices= INT_CHOICE ,verbose_name = "رضایت از چمران تیم")
    next_cooperatetion = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    fullfill_requirment = models.IntegerField(choices= INT_CHOICE ,verbose_name = "تامین مالی و ازمایشگاه")
    research_gain = models.IntegerField(choices= Gain_CHOICE,verbose_name = "دستاورد دانشجو")#//should be array
    
    def avarage(self):
        sum = 0.0
        sum = self.tech_enough_info + self.tech_required_info + self.totoal_gain + self.scientific_level
        sum = sum + self.availability + self.planing + self.formal_act + self.distribute_task
        + self.total_satisfaction + self.chamt_satisfaction + self.next_cooperatetion + self.fullfill_requirment

        ava = float(sum / 12)
        return ava
