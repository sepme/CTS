from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    project_form = models.OneToOneField(ProjectForm, on_delete=models.CASCADE) 
    date_submited_by_industry = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ ثبت پرژه توسط صنعت")
    date_selected_by_expert = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ درخواست پروژه توسط استاد")
    date_start = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ اخذ پروژه توسط استاد")
    date_project_started = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ شروع پروژه")
    date_pahse_two_deadline = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "ناریخ مهلت فاز دوم")
    date_pahse_three_deadline = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ مهلت فاز سوم")
    date_pahse_one_finished = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ پایان فاز اول")
    date_pahse_two_finished = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ پایان فاز دوم")
    date_finished = models.DateField(auto_now=False, auto_now_add=False,verbose_name = "تاریخ اتمام پروژه")
    researcher_applied = models.ManyToManyField(Researcher)
    researcher_accepted = models.ManyToManyField(Researcher, on_delete=models.CASCADE)
    expert_applied = models.ManyToManyField(Expert)
    expert_accepted = models.OneToOneField(Expert)
    industry_creator = models.OneToOneField(Industry, on_delete=models.CASCADE)
    cost_of_project = models.FloatField(verbose_name = "هزینه پروژه")
    maximum_researcher = models.IntegerField(verbose_name = "حداکثر تعداد پژوهشگر")   
    project_detail = models.CharField(max_length=None ,verbose_name = "جزيات پروژه")
    project_priority_level = models.FloatField(verbose_name ="سطح اهمیت پروژه")
    def __str__(self):
        return self.project_form.project_title_english

class ProjectForm(models.Model): 
    project_title_persian = models.CharField(max_length=None,verbose_name ="عنوان پروژه فارسی")
    project_title_english = models.CharField(max_length=None,verbose_name ="عنوان پروژه انگلیسی")
    key_words = models.CharField(max_length=None)
    percentage_wet_lab = models.FloatField(verbose_name ="درصد wet_lab")
    percentage_dry_lab = models.FloatField(,verbose_name ="درصد dry_lab ")
    research_methodology = models.CharField(max_length=None,verbose_name ="روش تحقیق")#need choices
    main_problem_and_importance = models.CharField(max_length=None,verbose_name ="مشکلات اصلی و اهداف")
    progress_profitability= models.CharField(max_length=None,verbose_name ="پیشرفا های حاصل")
    approach = models.CharField(max_length=None,verbose_name ="راه کار ها")
    innovation = models.CharField(max_length=None,verbose_name ="نو آوری ها")
    required_lab_equipment = models.CharField(max_length=None,verbose_name ="منابع مورد نیاز")
    reqired_technique = models.CharField(max_length=None,verbose_name ="تکنیک های مورد نیاز")
    project_phase =  models.CharField(max_length=None,verbose_name ="مراحل انجام پروژه")
    required_budget = models.FloatField(,verbose_name ="بودجه مورد نیاز")
    papers_and_documentaion = models.CharField(max_length=None,verbose_name ="مقالات و مستندات")
    policy = models.CharField(max_length=None,verbose_name ="نکات اخلاقی")

class Comment(models.Model):
    sender_comment = models.CharField(max_length=None)
    sender_choices = (('expert' ,'متخصص'),('industry' ,'صنعت'),)
    sender_type = models.CharField(max_length=15,choices = sender_choices)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attach_file = models.FileField(upload_to='./project_{0}'.format(project_title_english), max_length=100)

class Industry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    industry_form = models.OneToOneField(IndustryForm, on_delete=models.CASCADE) 
    research_field = models.CharField(max_length=None,verbose_name ="حوزه فعالیت")
    history_and_record = models.CharField(max_length=None,verbose_name ="",verbose_name ="سابقه")
    is_international_industry = models.BooleanField(max_length=None,verbose_name ="سابقه فعالیت بین المللی")
    industry_points = models.FloatField(verbose_name ="امتیاز صنعت")
    
    def __str__(self):
        return self.industry_name


class IndustryForm(models.Model):
    industry_name = models.CharField(max_length=None,verbose_name ="نام شرکت")
    registration_number = models.CharField(max_length=None,verbose_name ="شماره ثبت")
    date_of_foundation = models.DateField(auto_now=False, auto_now_add=False,verbose_name ="تاریخ تاسیس")
    industry_type = models.CharField(max_length=None,verbose_name ="نوع شرکت")#need choices
    industry_address = models.CharField(max_length=None,verbose_name ="ادرس شرکت")
    phone_number = models.IntegerField(verbose_name ="شماره تلفن")
    budget_for_research = models.FloatField(verbose_name ="بودجه برای تحقیقات")
    turn_over = models.FloatField(verbose_name ="گردش مالی")
    services_products = models.CharField(max_length=None,verbose_name ="خدمات/محصولات")
    awards_honors = models.CharField(max_length=None,verbose_name ="افتخارات")
    email_adress = models.EmailField(max_length=254و,verbose_name ="ادرس")


    
class ProjectHistory(models.Model):
    project_title_english = models.CharField(max_length=None)
    key_words = ManyToManyField(KeyWord)
    project_priority_level = models.FloatField(verbose_name ="")
    project_start_date = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ شروع")
    project_end_date = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ پایان")
    STATUS_CHOICE = (('completed' ,'completed'),('stoped' ,'stoped'),)
    project_status = models.CharField(max_length=9 ,choices = STATUS_CHOICE ,verbose_name="وضعیت")
    project_point = models.FloatField(verbose_name='امتیاز')
    project_income = models.IntegerField(verbose_name= 'درآمد')
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    
    def __str__(self):
        return "history of " + self.profile.name 
    
class Keyword(models.Model):
    key_word_name = models.CharField(max_length=None)
    
    
    
class ٍExepertEvaluation(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    expert  = models.OneToOneField(expert.Expert, on_delete=models.CASCADE)
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

    provide_material =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    provide_ensurance = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    ontime_payment = models.IntegerField(choices= INT_CHOICE ,verbose_name = " ")
    provide_place = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    formal_act = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    budget_amount = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    time_amount = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    total_satisfaction = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    chamt_satisfaction = models.IntegerField(choices= INT_CHOICE ,verbose_name = "")
    continue_coperate = models.BooleanField(choices= BOOL_CHOICE)
    using_chamt = models.BooleanField(choices= BOOL_CHOICE)
    to_paper = models.BooleanField(choices= BOOL_CHOICE)
    
    def avarage(self):
        sum = 0.0
        sum = self.provide_material + self.provide_ensurance + self.ontime_payment + self.provide_place
        sum = sum + self.formal_act + self.budget_amount + self.time_amount + self.chamt_satisfaction + self.total_satisfaction

        ava = float(sum / 9)
        return ava
    
