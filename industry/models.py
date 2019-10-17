import os
from ChamranTeamSite import settings
# from PIL import Image
from django.db import models
from django.contrib.auth.models import User

from django.shortcuts import reverse, HttpResponseRedirect
import uuid
from persiantools.jdatetime import JalaliDate


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
    projects = models.ManyToManyField('industry.Project', verbose_name='پروژه ها', blank=True)

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse("industry:index"))


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
    required_technique = models.ManyToManyField('researcher.Technique', verbose_name="تکنیک های مورد نیاز")
    required_technique = models.TextField(default='no technique', verbose_name='تکنیک های مورد نیاز')
    project_phase = models.TextField(verbose_name="مراحل انجام پروژه")
    required_budget = models.FloatField(verbose_name="بودجه مورد نیاز")
    policy = models.TextField(verbose_name="نکات اخلاقی")
    predict_profit = models.IntegerField(verbose_name='سود مالی')

    def __str__(self):
        return self.project_title_english


class Project(models.Model):
    project_form = models.OneToOneField(ProjectForm, on_delete=models.CASCADE, verbose_name="فرم پروژه")
    comments = models.ManyToManyField('industry.Comment', verbose_name='کامنت ها', null=True, blank=True)
    date_submitted_by_industry = models.DateField(verbose_name="تاریخ ثبت پرژه توسط صنعت", auto_now_add=True)
    date_selected_by_expert = models.DateField(verbose_name="تاریخ درخواست پروژه توسط استاد", null=True)
    date_start = models.DateField(verbose_name="تاریخ اخذ پروژه توسط استاد", null=True)
    date_project_started = models.DateField(verbose_name="تاریخ شروع پروژه", null=True)
    date_phase_two_deadline = models.DateField(verbose_name="ناریخ مهلت فاز دوم", null=True)
    date_phase_three_deadline = models.DateField(verbose_name="تاریخ مهلت فاز سوم", null=True)
    date_phase_one_finished = models.DateField(verbose_name="تاریخ پایان فاز اول", null=True)
    date_phase_two_finished = models.DateField(verbose_name="تاریخ پایان فاز دوم", null=True)
    date_finished = models.DateField(verbose_name="تاریخ اتمام پروژه", null=True)
    researcher_applied = models.ManyToManyField('researcher.ResearcherUser', verbose_name="پژوهشگران درخواست داده",
                                                related_name="researchers_applied", blank=True, null=True)
    researcher_accepted = models.ManyToManyField('researcher.ResearcherUser', verbose_name="پژوهشگران پذبرفته شده",
                                                 related_name="researchers_accepted", blank=True, null=True)
    expert_applied = models.ManyToManyField('expert.ExpertUser', verbose_name="اساتید درخواست داده",
                                            related_name="experts_applied", blank=True, null=True)
    expert_accepted = models.OneToOneField('expert.ExpertUser', on_delete=models.CASCADE,
                                           verbose_name="استاد پذیرفته شده", related_name="expert_accepted", blank=True,
                                           null=True)
    cost_of_project = models.IntegerField(verbose_name="هزینه پروژه", null=True)
    maximum_researcher = models.IntegerField(verbose_name="حداکثر تعداد پژوهشگر", null=True)
    project_detail = models.TextField(verbose_name="جزيات پروژه", null=True)
    project_priority_level = models.FloatField(verbose_name="سطح اهمیت پروژه", null=True)

    def __str__(self):
        return self.project_form.project_title_english

    def get_comments(self):
        project_comments = Comment.objects.all().filter(project=self)
        return project_comments

    class Meta:
        ordering = ['-date_submitted_by_industry']


def upload_comment(instance, file_name):
    return os.path.join(settings.MEDIA_ROOT, instance.project.__str__(), file_name)


class Comment(models.Model):
    description = models.TextField(verbose_name="متن")
    SENDER = (
        (0, 'متخصص'),
        (1, 'صنعت')
    )
    sender_type = models.IntegerField(choices=SENDER)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    attachment = models.FileField(upload_to=upload_comment)
    date_submitted = models.DateField(auto_now_add=True, verbose_name="تاریخ ثبت")


class ProjectHistory(models.Model):
    project_title_english = models.CharField(max_length=128)
    keywords = models.ManyToManyField(Keyword, verbose_name="کلمات کلیدی")
    project_priority_level = models.FloatField(verbose_name="میزان اهمیت پروژه")
    project_start_date = models.DateField(verbose_name="تاریخ شروع")
    project_end_date = models.DateField(verbose_name="تاریخ پایان")
    STATUS_CHOICE = (
        (0, 'completed'),
        (1, 'stoped')
    )
    project_status = models.IntegerField(choices=STATUS_CHOICE, verbose_name="وضعیت")
    project_point = models.FloatField(verbose_name='امتیاز')
    project_income = models.IntegerField(verbose_name='درآمد')
    industry = models.ForeignKey(IndustryUser, on_delete=models.CASCADE)

    def __str__(self):
        return "history of " + self.project_title_english


class ExpertEvaluateIndustry(models.Model):
    industry = models.ForeignKey(IndustryUser, on_delete=models.CASCADE)
    expert = models.OneToOneField('expert.ExpertUser', on_delete=models.CASCADE, blank=True, null=True)
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
