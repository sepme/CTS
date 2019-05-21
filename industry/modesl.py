from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    project_form = models.OneToOneField(ProjectForm, on_delete=models.CASCADE) 
    date_submited_by_industry = models.DateField(auto_now=False, auto_now_add=False)
    date_selected_by_expert = models.DateField(auto_now=False, auto_now_add=False)
    date_start = models.DateField(auto_now=False, auto_now_add=False)
    date_project_started = models.DateField(auto_now=False, auto_now_add=False)
    date_pahse_two_deadline = models.DateField(auto_now=False, auto_now_add=False)
    date_pahse_three_deadline = models.DateField(auto_now=False, auto_now_add=False)
    date_pahse_one_finished = models.DateField(auto_now=False, auto_now_add=False)
    date_pahse_two_finished = models.DateField(auto_now=False, auto_now_add=False)
    date_finished = models.DateField(auto_now=False, auto_now_add=False)
    researcher_applied = models.ManyToManyField(Researcher)
    researcher_accepted = models.OneToOneField(Researcher, on_delete=models.CASCADE)
    expert_applied = models.ManyToManyField(Expert)
    expert_accepted = models.ManyToManyField(Expert)
    industry_creator = models.OneToOneField(Industry, on_delete=models.CASCADE)
    cost_of_project = models.FloatField()
    maximum_researcher = models.IntegerField()   
    project_detail = models.CharField(max_length=None)
    project_priority_level = models.FloatField()
    def __str__(self):
        return self.project_form.project_title_english

class ProjectForm(models.Model): 
    project_title_persian = models.CharField(max_length=None)
    project_title_english = models.CharField(max_length=None)
    key_words = models.CharField(max_length=None)
    percentage_wet_lab = models.FloatField()
    percentage_dry_lab = models.FloatField()
    research_methodology = models.CharField(max_length=None)
    main_problem_and_importance = models.CharField(max_length=None)
    progress_profitability= models.CharField(max_length=None)
    approach = models.CharField(max_length=None)
    innovation = models.CharField(max_length=None)
    required_lab_equipment = models.CharField(max_length=None)
    reqired_technique = models.CharField(max_length=None)
    project_phase =  models.CharField(max_length=None)
    required_budget = models.FloatField()
    papers_and_documentaion = models.CharField(max_length=None)
    policy = models.CharField(max_length=None)

class Comment(models.Model):
    sender_comment = models.CharField(max_length=None)
    sender_choices = (('expert' ,'متخصص'),('industry' ,'صنعت'),)
    sender_type = models.CharField(max_length=15,choices = sender_choices)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attach_file = models.FileField(upload_to='./project_{0}'.format(project_title_english), max_length=100)

class Industry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    industry_form = models.OneToOneField(IndustryForm, on_delete=models.CASCADE) 
    research_field = models.CharField(max_length=None)
    history_and_record = models.CharField(max_length=None)
    is_international_industry = models.BooleanField(max_length=None)
    industry_points = models.FloatField()
    project_history = models.ForeignKey(ProjectHistory, on_delete=models.CASCADE)
    def __str__(self):
        return self.industry_name


class IndustryForm(models.Model):
    industry_name = models.CharField(max_length=None)
    registration_number = models.CharField(max_length=None)
    date_of_foundation = models.DateField(auto_now=False, auto_now_add=False)
    industry_type = models.CharField(max_length=None)
    industry_address = models.CharField(max_length=None)
    phone_number = models.IntegerField()
    budget_for_research = models.FloatField()
    turn_over = models.FloatField()
    services_products = models.CharField(max_length=None)
    awards_honors = models.CharField(max_length=None)
    email_adress = models.EmailField(max_length=254)


    
class ProjectHistory(models.Model):
    project_title_english = models.CharField(max_length=None)
    key_words = ManyToManyField(KeyWord)
    project_priority_level = models.FloatField()
    project_start_date = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ شروع")
    project_end_date = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ پایان")
    STATUS_CHOICE = (
        ('completed' ,'completed'),
        ('stoped' ,'stoped'),
    )
    project_status = models.CharField(max_length=9 ,choices = STATUS_CHOICE ,verbose_name="وضعیت")
    project_point = models.FloatField(verbose_name='امتیاز')
    project_income = models.IntegerField(verbose_name= 'درآمد')
  
    def __str__(self):
        return "history of " + self.profile.name 
    
class KeyWord(models.Model):
    key_word_name = models.CharField(max_length=None)
