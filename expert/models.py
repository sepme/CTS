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
    expert_firstname = models.CharField(max_length=None,verbose_name = "")
    expert_lastname = models.CharField(max_length=None,verbose_name = "")
    special_field = models.CharField(max_length=None,verbose_name = "")
    national_code = models.IntegerField(verbose_name = "")
    scientific_rank = models.CharField(max_length=None,verbose_name = "")
    university = models.CharField(max_length=None,verbose_name = "")
    home_adress = models.CharField(max_length=None,verbose_name = "")
    phone_number = models.IntegerField(verbose_name = "")
    mobile_phone =  models.IntegerField(verbose_name = "")
    email_adress = models.EmailField(max_length=254,verbose_name = "")
    eq_tset = models.OneToOneField(EqTset, on_delete=models.CASCADE,verbose_name = "")
    awards = models.CharField(max_length=None,verbose_name = "")
    method_of_introduction = models.CharField(max_length=None,verbose_name = "")
    posetive_feature_chamt =  models.CharField(max_length=None,verbose_name = "")
    lab_equipment = models.CharField(max_length=None,verbose_name = "")
    number_of_resercher = models.IntegerField(verbose_name = "")
    has_indusryial_researech = models.BooleanField(verbose_name = "")
    number_of_grants = models.IntegerField(verbose_name = "")
    technique =  models.ManyToManyField(researcher.Technique,verbose_name = "")
    languages = models.CharField(max_length=None,verbose_name = "")

class ScientificRecord(models.Model):
    degree = models.CharField(max_length=None,verbose_name = "")
    major = models.CharField(max_length=None,verbose_name = "")
    university = models.CharField(max_length=None,verbose_name = "")
    city = models.CharField(max_length=None,verbose_name = "")
    date_of_grauate = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "")
    expert_form =  models.ForeignKey(ExpertForm, on_delete=models.CASCADE,verbose_name = "فرم استاد")
    
class ExecutiveRecord(models.Model):
    executive_post = models.CharField(max_length=None,verbose_name = "")
    date_start_post = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "")
    date_end_post = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "")
    city =  models.CharField(max_length=None,verbose_name = "")
    organization =  models.CharField(max_length=None,verbose_name = "")
    expert_form =  models.ForeignKey(ExpertForm, on_delete=models.CASCADE,verbose_name = "فرم استاد")

class ResearchRecord(models.Model):
    research_title = models.CharField(max_length=None,verbose_name = "")
    researcher = models.CharField(max_length=None,verbose_name = "")
    co_researcher = models.CharField(max_length=None,verbose_name = "")
    status = models.CharField(max_length=None,verbose_name = "")
    expert_form =  models.ForeignKey(ExpertForm, on_delete=models.CASCADE,verbose_name = "فرم استاد")

class PaperRecord(models.Model):
    research_title = models.CharField(max_length=None,verbose_name = "")
    date_published = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "")
    publised_at = models.CharField(max_length=None,verbose_name = "")
    impact_factor = models.FloatField(verbose_name = "")
    citation = models.IntegerField(verbose_name = "")
    expert_form =  models.ForeignKey(ExpertForm, on_delete=models.CASCADE,verbose_name = "فرم استاد")
    
class EqTset(models.Model):
    team_work = models.IntegerField(verbose_name = "")
    innovation = models.IntegerField(verbose_name = "")
    devtion = models.IntegerField(verbose_name = "")
    productive_research = models.IntegerField(verbose_name = "")
    national_commitment = models.IntegerField(verbose_name = "")
    collecting_information = models.IntegerField(verbose_name = "")
    business_thinking = models.IntegerField(verbose_name = "")
    risk_averse = models.IntegerField(verbose_name = "")

class Technique(models.Model):
    technique_name = models.CharField(max_length=None,verbose_name = "")
    ready_to_teach =  models.BooleanField(verbose_name = "")
    skill_level = models.CharField(max_length=None,verbose_name = "")

class ExpertProjectHistory(models.Model):
    project_title_english = models.CharField(max_length=None,verbose_name = "")
    key_words = models.CharField(max_length=None,verbose_name = "")
    project_priority_level = models.FloatField(verbose_name = "")
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
    
    
class IndustryEvaluation(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE,verbose_name = "")
    industry  = models.OneToOneField(industry.Industry, on_delete=models.CASCADE,verbose_name = "")
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

    ontime_progress_report =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    cotribution_to_industry = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    corect_estimation = models.IntegerField(choices= INT_CHOICE ,verbose_name = " ")
    ontime_deadline = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    fullfill_requirment = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    diciplined = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    comited_to_goals = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    quality = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    total_satisfaction = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    continue_coperate = models.BooleanField(choices= BOOL_CHOICE)
    using_chamt = models.BooleanField(choices= BOOL_CHOICE)
    has_inovation = models.BooleanField(choices= BOOL_CHOICE)
    
    def avarage(self):
        sum = 0.0
        sum = self.ontime_progress_report + self.cotribution_to_industry + self.corect_estimation + self.ontime_deadline
        sum = sum + self.fullfill_requirment + self.comited_to_goals + self.total_satisfaction + self.quality + self.diciplined

        ava = float(sum / 8)
        return ava
    
class ResearcherEvaluation(models.Model):
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

    tech_enough_info =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    tech_required_info = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    totoal_gain = models.IntegerField(choices= INT_CHOICE ,verbose_name = " ")
    scientific_level = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    availability = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    planing = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    formal_act = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    distribute_task = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    total_satisfaction = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    chamt_satisfaction = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    next_cooperatetion = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    fullfill_requirment = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    research_gain = models.IntegerField(choices= Gain_CHOICE)#//should be array
    
    def avarage(self):
        sum = 0.0
        sum = self.tech_enough_info + self.tech_required_info + self.totoal_gain + self.scientific_level
        sum = sum + self.availability + self.planing + self.formal_act + self.distribute_task
        + self.total_satisfaction + self.chamt_satisfaction + self.next_cooperatetion + self.fullfill_requirment

        ava = float(sum / 12)
        return ava
