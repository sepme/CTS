from django.db import models
from django.contrib.auth.models import User

class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expert_form = models.OneToOneField(ExpertForm, on_delete=models.CASCADE) 
    date_register = models.DateField(auto_now=False, auto_now_add=False)
    expert_project_history = models.ForeignKey(ExpertProjectHistory, on_delete=models.CASCADE)
    expert_point = models.IntegerField()
    def __str__(self):
        return self.expert_form.expert_firstname+self.expert_form.expert_lastname

class ExpertForm(models.Model): 
    expert_firstname = models.CharField(max_length=None)
    expert_lastname = models.CharField(max_length=None)
    special_field = models.CharField(max_length=None)
    national_code = models.IntegerField()
    scientific_rank = models.CharField(max_length=None)
    university = models.CharField(max_length=None)
    home_adress = models.CharField(max_length=None)
    phone_number = models.IntegerField()
    mobile_phone =  models.IntegerField()
    email_adress = models.EmailField(max_length=254)
    scientific_record =  models.ForeignKey(ScientificRecord, on_delete=models.CASCADE)
    executive_record =  models.ForeignKey(ExecutiveRecord, on_delete=models.CASCADE)
    research_record =  models.ForeignKey(ResearchRecord, on_delete=models.CASCADE)
    paper_record =  models.ForeignKey(PaperRecord, on_delete=models.CASCADE)
    eq_tset = models.OneToOneField(EqTset, on_delete=models.CASCADE)
    awards = models.CharField(max_length=None)
    method_of_introduction = models.CharField(max_length=None)
    posetive_feature_chamt =  models.CharField(max_length=None)
    lab_equipment = models.CharField(max_length=None)
    number_of_resercher = models.IntegerField()
    has_indusryial_researech = models.BooleanField()
    number_of_grants = models.IntegerField()
    technique =  models.ForeignKey(researcher.Technique, on_delete=models.CASCADE)
    languages = models.CharField(max_length=None)

class ScientificRecord(models.Model):
    degree = models.CharField(max_length=None)
    major = models.CharField(max_length=None)
    university = models.CharField(max_length=None)
    city = models.CharField(max_length=None)
    date_of_grauate = models.DateField(auto_now=False, auto_now_add=False)

class ExecutiveRecord(models.Model):
    executive_post = models.CharField(max_length=None)
    date_start_post = models.DateField(auto_now=False, auto_now_add=False)
    date_end_post = models.DateField(auto_now=False, auto_now_add=False)
    city =  models.CharField(max_length=None)
    organization =  models.CharField(max_length=None)

class ResearchRecord(models.Model):
    research_title = models.CharField(max_length=None)
    researcher = models.CharField(max_length=None)
    co_researcher = models.CharField(max_length=None)
    status = models.CharField(max_length=None)

class PaperRecord(models.Model):
    research_title = models.CharField(max_length=None)
    date_published = models.DateField(auto_now=False, auto_now_add=False)
    publised_at = models.CharField(max_length=None)
    impact_factor = models.FloatField()
    citation = models.IntegerField()

class EqTset(models.Model):
    team_work = models.IntegerField()
    innovation = models.IntegerField()
    devtion = models.IntegerField()
    productive_research = models.IntegerField()
    national_commitment = models.IntegerField()
    collecting_information = models.IntegerField()
    business_thinking = models.IntegerField()
    risk_averse = models.IntegerField()

class Technique(models.Model):
    technique_name = models.CharField(max_length=None)
    ready_to_teach =  models.BooleanField()
    skill_level = models.CharField(max_length=None)

class ExpertProjectHistory(models.Model):
    project_title_english = models.CharField(max_length=None)
    key_words = models.CharField(max_length=None)
    project_priority_level = models.FloatField()
