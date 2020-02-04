import os
import datetime
from dateutil.relativedelta import relativedelta

from ChamranTeamSite import settings
# from PIL import Image
from django.db import models
from django.contrib.auth.models import User

from django.shortcuts import reverse, HttpResponseRedirect
import uuid
from persiantools.jdatetime import JalaliDate

from researcher.models import ResearcherUser ,RequestedProject ,Technique
from expert import models as expertModels

'''
Each IndustryUser object has a one-to-one field to django's User model, an industryform contaning his information,
and projects.
Each Project object has a projectform field containing the information about the project like the required budget,
skills, etc. The other fields of Project indicate who is going to do it and when they are going to do it. 
For comments it's simple: we create a record for every comment and when we need to display the comments on a project
with just search through the Comments for the ones sent by the the users we're looking for and on the project we want.
ProjectHistory objects are the summary of a project that's been done and we don't need all its details anymore, so we 
delete the Project object and only keep its main information in a ProjectHistory object.
'''
class IndustryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر صنعت")
    industry_points = models.FloatField(verbose_name="امتیاز صنعت", default=0.0)
    industryform = models.OneToOneField('industry.IndustryForm', blank=True, null=True, on_delete=models.CASCADE,
                                        verbose_name="فرم صنعت")
    STATUS = (
        ('signed_up', "فرم های مورد نیاز تکمیل نشده است. "),
        ('free', "فعال - بدون پروژه"),
        ('involved', "فعال - درگیر پروژه"),
        ('inactivated', "غیر فعال - تویط مدیر سایت غیر فعال شده است."),
    )
    status = models.CharField(max_length=15, choices=STATUS, default='signed_up')
    unique = models.UUIDField(unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse("industry:index"))

    @property
    def score(self):
        return self.industry_points*23
# def upload_and_rename_profile(instance, file_name):
#     return os.path.join('{}/'.format(instance.name), 'profile.{}'.format(file_name.split('.')[-1]))


def unique_upload(instance, file_name):
    return os.path.join('{}/'.format(instance.name), file_name)


class IndustryForm(models.Model):
    name = models.CharField(max_length=64, verbose_name="نام شرکت")
    registration_number = models.IntegerField(verbose_name="شماره ثبت")
    date_of_foundation = models.IntegerField(verbose_name="تاریخ تاسیس")
    research_field = models.CharField(max_length=32, verbose_name="حوزه فعالیت")
    industry_type_choice = (
        (0, 'خصوصی'),
        (1, 'دولتی'),
    )
    industry_type = models.IntegerField(choices=industry_type_choice, blank=False, null=False, verbose_name="نوع شرکت")
    industry_address = models.TextField(verbose_name="ادرس شرکت")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    # international_activities = models.TextField(null=True, verbose_name="سابقه فعالیت بین المللی")
    tax_declaration = models.FileField(null=True, blank=True, upload_to=unique_upload, verbose_name="اظهارنامه مالیاتی")
    # turn_over = models.FloatField(null=True, verbose_name="گردش مالی")
    services_products = models.TextField(null=True, blank=True, verbose_name="خدمات/محصولات")
    awards_honors = models.TextField(null=True, blank=True, verbose_name="افتخارات")
    email_address = models.EmailField(max_length=254, verbose_name="ادرس")
    photo = models.ImageField(upload_to=unique_upload, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save()
        if self.photo:
            if '\\' in self.photo.name:
                self.photo.name = self.photo.name.split('\\')[-1]
            elif '/' in self.photo.name:
                self.photo.name = self.photo.name.split('/')[-1]
        super().save()


class Keyword(models.Model):
    name = models.CharField(max_length=32, primary_key=True)

    def __str__(self):
        return self.name.__str__()


class ProjectForm(models.Model):
    key_words = models.ManyToManyField(Keyword, verbose_name="کلمات کلیدی")
    project_title_persian = models.CharField(max_length=128, verbose_name="عنوان پروژه فارسی")
    project_title_english = models.CharField(max_length=128, verbose_name="عنوان پروژه انگلیسی")
    research_methodology_choice = (
        (0, 'کیفی'),
        (1, 'کمی'),
    )
    research_methodology = models.IntegerField(choices=research_methodology_choice, verbose_name="روش تحقیق")
    main_problem_and_importance = models.TextField(verbose_name="مشکلات اصلی و اهداف")
    progress_profitability = models.TextField(verbose_name="پیشرفت های حاصل")
    approach = models.TextField(verbose_name="راه کار ها")
    potential_problems = models.TextField(verbose_name='مشکلات احتمالی')
    required_lab_equipment = models.TextField(verbose_name="منابع مورد نیاز")
    required_method = models.TextField(verbose_name="روش های مورد نیاز" ,null=True)
    project_phase = models.TextField(verbose_name="مراحل انجام پروژه")
    required_budget = models.IntegerField(verbose_name="بودجه مورد نیاز")
    policy = models.TextField(verbose_name="نکات اخلاقی")
    predict_profit = models.IntegerField(verbose_name='سود مالی')

    def __str__(self):
        return self.project_title_english

    @property
    def required_technique(self):
        expert_requested = expertModels.ExpertRequestedProject.objects.all().filter(project=self.project).filter(expert=self.project.expert_accepted).first()
        return expert_requested.required_technique.all()

class Project(models.Model):
    project_form = models.OneToOneField(ProjectForm, on_delete=models.CASCADE, verbose_name="فرم پروژه")
    date_submitted_by_industry = models.DateField(verbose_name="تاریخ ثبت پرژه توسط صنعت", auto_now_add=True)
    date_selected_by_expert = models.DateField(verbose_name="تاریخ درخواست پروژه توسط استاد", null=True, blank=True)
    date_start = models.DateField(verbose_name="تاریخ اخذ پروژه توسط استاد", null=True, blank=True)
    date_project_started = models.DateField(verbose_name="تاریخ شروع پروژه", null=True, blank=True)
    date_phase_two_deadline = models.DateField(verbose_name="ناریخ مهلت فاز دوم", null=True, blank=True)
    date_phase_three_deadline = models.DateField(verbose_name="تاریخ مهلت فاز سوم", null=True, blank=True)
    date_phase_one_finished = models.DateField(verbose_name="تاریخ پایان فاز اول", null=True, blank=True)
    date_phase_two_finished = models.DateField(verbose_name="تاریخ پایان فاز دوم", null=True, blank=True)
    date_finished = models.DateField(verbose_name="تاریخ اتمام پروژه", null=True, blank=True)
    researcher_applied = models.ManyToManyField('researcher.ResearcherUser', through='researcher.RequestedProject',
                                                verbose_name="پژوهشگران درخواست داده",
                                                related_name="researchers_applied", blank=True)
    researcher_accepted = models.ManyToManyField('researcher.ResearcherUser', verbose_name="پژوهشگران پذبرفته شده",
                                                 related_name="researchers_accepted", blank=True)
    expert_applied = models.ManyToManyField('expert.ExpertUser', through='expert.ExpertRequestedProject',
                                            verbose_name="اساتید درخواست داده",
                                            related_name="experts_applied", blank=True)
    expert_accepted = models.ForeignKey('expert.ExpertUser', on_delete=models.CASCADE, verbose_name="استاد پذیرفته "
                                                                                                    "شده",
                                        related_name="expert_accepted", blank=True, null=True)
    expert_messaged = models.ManyToManyField('expert.ExpertUser', blank=True,
                                             verbose_name='اساتیدی که پیام داده اند')
    industry_creator = models.ForeignKey('industry.IndustryUser', on_delete=models.CASCADE,
                                         null=True, blank=True, verbose_name='شرکت '
                                                                             'صاحب '
                                                                             'پروژه')
    cost_of_project = models.FloatField(verbose_name="هزینه پروژه", null=True, blank=True)
    maximum_researcher = models.IntegerField(verbose_name="حداکثر تعداد پژوهشگر", null=True, blank=True)
    project_detail = models.TextField(verbose_name="جزيات پروژه", null=True, blank=True)
    project_priority_level = models.FloatField(verbose_name="سطح اهمیت پروژه", null=True, blank=True)
    PROJECT_STATUS_CHOICES = (
        (0, 'در حال بررسی'),
        (1, 'فعال'),
        (2, 'معلق'),
        (3, 'انجام شد'),
        (4, 'در حال انتظار')
    )
    status = models.IntegerField(choices=PROJECT_STATUS_CHOICES, verbose_name='وضعیت پروژه', default=0, blank=True)

    def __str__(self):
        return self.project_form.project_title_english

    def get_comments(self):
        project_comments = Comment.objects.all().filter(project=self)
        return project_comments

    @property
    def time_left(self):
        delta = relativedelta(self.date_finished, datetime.date.today())
        if delta.years != 0:
            return str(delta.years) + ' سال'
        elif delta.months != 0:
            return str(delta.months) + ' ماه'
        elif delta.days != 0:
            return str(delta.days) + ' روز'
        else:
            return 'امروز'

    @property
    def industryUnseenCommentCount(self):
        expert_unseen = Comment.objects.filter(sender_type='expert').filter(status='unseen').filter(industry_user=self.industry_creator).count()
        system_unseen = Comment.objects.filter(sender_type='system').filter(status='unseen').filter(industry_user=self.industry_creator).count()
        return expert_unseen + system_unseen

    class Meta:
        ordering = ['-date_submitted_by_industry']


def upload_comment(instance, file_name):
    return os.path.join(settings.MEDIA_ROOT, instance.project.__str__(), file_name)


class Comment(models.Model):
    description = models.TextField(verbose_name="متن")
    SENDER = (
        ("expert", 'استاد'),
        ("industry", 'صنعت'),
        ("researcher", 'پژوهشگر'),
        ("system", 'سیستم'),
    )
    replied_text = models.CharField(max_length=150, blank=True, null=True)
    sender_type = models.CharField(max_length=10 ,choices=SENDER)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, blank=True, null=True)
    industry_user = models.ForeignKey(IndustryUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    expert_user = models.ForeignKey('expert.ExpertUser', on_delete=models.DO_NOTHING, null=True, blank=True)
    researcher_user = models.ForeignKey(ResearcherUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    attachment = models.FileField(upload_to=upload_comment, blank=True, null=True)
    date_submitted = models.DateField(auto_now_add=True, verbose_name="تاریخ ثبت")
    STATUS=(
        ('seen', 'seen'),
        ('unseen' ,'unseen'),
    )
    status = models.CharField(max_length=6, choices=STATUS, null=True)

    def __str__(self):
        return self.sender_type + " - " + str(self.project)

class ProjectHistory(models.Model):
    project_title_english = models.CharField(max_length=128)
    keywords = models.ManyToManyField(Keyword, verbose_name="کلمات کلیدی")
    project_priority_level = models.FloatField(verbose_name="میزان اهمیت پروژه")
    project_start_date = models.DateField(verbose_name="تاریخ شروع")
    project_end_date = models.DateField(verbose_name="تاریخ پایان")
    STATUS_CHOICE = (
        (0, 'completed'),
        (1, 'stopped')
    )
    project_status = models.IntegerField(choices=STATUS_CHOICE, verbose_name="وضعیت")
    project_point = models.FloatField(verbose_name='امتیاز')
    project_income = models.IntegerField(verbose_name='درآمد')
    industry = models.ForeignKey(IndustryUser, on_delete=models.CASCADE)

    def __str__(self):
        return "history of " + self.project_title_english


class ExpertEvaluateIndustry(models.Model):
    industry = models.ForeignKey(IndustryUser, on_delete=models.CASCADE)
    project  = models.ForeignKey(Project ,on_delete=models.CASCADE ,null=True)
    expert = models.ForeignKey('expert.ExpertUser', on_delete=models.CASCADE, blank=True, null=True)
    phase = models.IntegerField(verbose_name="فاز شماره : " ,null=True)
    INT_CHOICE = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    BOOL_CHOICE = (
        (False, "false"),
        (True, "true"),
    )

    provide_material = models.IntegerField(choices=INT_CHOICE, verbose_name="رضایت از تامین مواد اولیه")
    provide_insurance = models.IntegerField(choices=INT_CHOICE, verbose_name="رضایت از بیمه کارکنان")
    punctuality = models.IntegerField(choices=INT_CHOICE, verbose_name="نحوه پرداخت به موقع")
    provide_place = models.IntegerField(choices=INT_CHOICE, verbose_name="تامین محل انجام")
    formal_act = models.IntegerField(choices=INT_CHOICE, verbose_name="برخورد محترمانه")
    budget_amount = models.IntegerField(choices=INT_CHOICE, verbose_name="بودجه سازگار با واقعیت")
    time_amount = models.IntegerField(choices=INT_CHOICE, verbose_name="زمان بندی مطابق خواسته ها")
    total_satisfaction = models.IntegerField(choices=INT_CHOICE, verbose_name="رضایت کلی")
    chamt_satisfaction = models.IntegerField(choices=INT_CHOICE, verbose_name="عملکرد چمران تیم")
    continue_cooperate = models.BooleanField(choices=BOOL_CHOICE, verbose_name="ادامه همکاری با صنعت")
    using_chamt = models.BooleanField(choices=BOOL_CHOICE, verbose_name="ادامه همکاری با چمران تیم")
    to_paper = models.BooleanField(choices=BOOL_CHOICE, verbose_name="قابلیت تبدیل به مقاله")

    def average(self):
        sum = 0.0
        sum = self.provide_material + self.provide_insurance + self.punctuality + self.provide_place
        sum = sum + self.formal_act + self.budget_amount + self.time_amount + self.chamt_satisfaction + self.total_satisfaction

        ava = float(sum / 9)
        return ava

    def __str__(self):
        return str(self.industry) + " evaluate " + str(self.expert.expertform)
