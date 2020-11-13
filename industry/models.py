import os
import datetime
from dateutil.relativedelta import relativedelta

from ChamranTeamSite import settings
from django.db import models
from django.contrib.auth.models import User

from django.shortcuts import reverse, HttpResponseRedirect
import uuid
from persiantools.jdatetime import JalaliDate

# for Compress the photo
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from researcher.models import ResearcherUser, RequestedProject, Technique
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
    userId = models.CharField(max_length=50, verbose_name="ID کاربر", blank=True, null=True)
    industry_points = models.FloatField(verbose_name="امتیاز صنعت", default=0.0)
    STATUS = (
        ('signed_up', "فرم های مورد نیاز تکمیل نشده است. "),
        ('free', "فعال - بدون پروژه"),
        ('involved', "فعال - درگیر پروژه"),
        ('inactivated', "غیر فعال - تویط مدیر سایت غیر فعال شده است."),
    )
    status = models.CharField(max_length=15, choices=STATUS, default='signed_up')
    unique = models.UUIDField(unique=True, default=uuid.uuid4)
    chat_id = models.CharField(verbose_name="آیدی چت", max_length=50, null=True, blank=True)

    class Meta:
        permissions = (
            ('be_industry', 'Be Industry'),
        )

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse("industry:index"))

    def get_name(self):
        try:
            return self.randdprofile.name
        except:
            return self.researchgroupprofile.name

    @property
    def profile(self):
        try:
            return self.randdprofile
        except:
            return self.researchgroupprofile

    @property
    def score(self):
        return self.industry_points * 23

    @property
    def industry_type(self):
        if RandDProfile.objects.filter(industry_user=self).exists():
            return "R&D"
        else:
            return "researchGroup"

# def upload_and_rename_profile(instance, file_name):
#     return os.path.join('{}/'.format(instance.name), 'profile.{}'.format(file_name.split('.')[-1]))


def profileUpload(instance, file_name):
    return os.path.join('Industry Profile', instance.industry_user.user.username, file_name)


class IndustryForm(models.Model):
    industry_user = models.OneToOneField(IndustryUser, blank=True, null=True, on_delete=models.CASCADE,
                                         verbose_name="صنعت")
    name = models.CharField(max_length=128, verbose_name="نام شرکت")
    registration_number = models.CharField(max_length=10, verbose_name="شماره ثبت")
    date_of_foundation = models.CharField(max_length=4, verbose_name="تاریخ تاسیس")
    research_field = models.CharField(max_length=128, verbose_name="حوزه فعالیت")
    industry_type_choice = (
        (0, 'خصوصی'),
        (1, 'دولتی'),
    )
    industry_type = models.IntegerField(choices=industry_type_choice, blank=False, null=False, verbose_name="نوع شرکت")
    industry_address = models.TextField(verbose_name="ادرس شرکت")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    # international_activities = models.TextField(null=True, verbose_name="سابقه فعالیت بین المللی")
    tax_declaration = models.FileField(null=True, blank=True, upload_to=profileUpload, verbose_name="اظهارنامه مالیاتی")
    # turn_over = models.FloatField(null=True, verbose_name="گردش مالی")
    services_products = models.TextField(null=True, blank=True, verbose_name="خدمات/محصولات")
    awards_honors = models.TextField(null=True, blank=True, verbose_name="افتخارات")
    photo = models.ImageField(upload_to=profileUpload, max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id:
            perv = IndustryForm.objects.get(id=self.id)
            if perv.photo.name:
                if self.photo.name.split("/")[-1] != perv.photo.name.split("/")[-1]:
                    self.photo = self.compressImage(self.photo)
            else:
                if self.photo.name:
                    self.photo = self.compressImage(self.photo)
        else:
            if self.photo.name:
                self.photo = self.compressImage(self.photo)
        super(IndustryForm, self).save(*args, **kwargs)
 
    def compressImage(self, photo):
        imageTemproary = Image.open(photo).convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='JPEG', quality=40)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % photo.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage


class InterfacePerson(models.Model):
    fullname = models.CharField(max_length=150, verbose_name='نام و نام خانوادگی')
    position = models.CharField(verbose_name="سمت", max_length=150)
    phone_number = models.CharField(verbose_name="شماره همراه", max_length=11)
    email = models.EmailField(verbose_name="پست الکترونیکی", max_length=254)

    def __str__(self):
        return self.fullname


class RandDProfile(models.Model):
    industry_user = models.OneToOneField(IndustryUser, blank=True, null=True, on_delete=models.CASCADE,
                                         verbose_name="صنعت")
    interfacePerson = models.OneToOneField("InterfacePerson", verbose_name='شخص رابط', on_delete=models.CASCADE)
    # RandDname = models.CharField(max_length=64, verbose_name="نام شرکت")
    name = models.CharField(max_length=128, verbose_name="نام شرکت", null=True)
    photo = models.ImageField(upload_to=profileUpload, max_length=256, blank=True, null=True)
    registration_number = models.CharField(max_length=10, verbose_name="شماره ثبت")
    date_of_foundation = models.CharField(max_length=4, verbose_name="تاریخ تاسیس")
    research_field = models.CharField(max_length=128, verbose_name="حوزه فعالیت")
    RandD_type_choice = (
        (0, 'خصوصی'),
        (1, 'دولتی'),
    )
    RandD_type = models.IntegerField(choices=RandD_type_choice, blank=False, null=False, verbose_name="نوع شرکت")
    address = models.TextField(verbose_name="ادرس شرکت")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن")
    # international_activities = models.TextField(null=True, verbose_name="سابقه فعالیت بین المللی")
    tax_declaration = models.FileField(null=True, blank=True, upload_to=profileUpload, verbose_name="اظهارنامه مالیاتی")
    # turn_over = models.FloatField(null=True, verbose_name="گردش مالی")
    services_products = models.TextField(null=True, blank=True, verbose_name="خدمات/محصولات")
    awards_honors = models.TextField(null=True, blank=True, verbose_name="افتخارات")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id:
            perv = RandDProfile.objects.get(id=self.id)
            if perv.photo.name:
                if self.photo.name.split("/")[-1] != perv.photo.name.split("/")[-1]:
                    self.photo = self.compressImage(self.photo)
            else:
                if self.photo.name:
                    self.photo = self.compressImage(self.photo)
        else:
            if self.photo.name:
                self.photo = self.compressImage(self.photo)
        super(RandDProfile, self).save(*args, **kwargs)

    def compressImage(self, photo):
        imageTemproary = Image.open(photo).convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='JPEG', quality=40)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % photo.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage


class ResearchGroupProfile(models.Model):
    industry_user = models.OneToOneField(IndustryUser, verbose_name="کاربر صنعت", on_delete=models.CASCADE)
    interfacePerson = models.OneToOneField(InterfacePerson, verbose_name="فرد رابط", on_delete=models.CASCADE)
    name = models.CharField("نام مرکز", max_length=150)
    photo = models.ImageField(upload_to=profileUpload, max_length=256, null=True, blank=True)
    address = models.TextField(verbose_name="ادرس", max_length=1000)
    phone_number = models.CharField(verbose_name="شماره تلفن", max_length=11)
    subordinateResearch = models.CharField(verbose_name="پژوهشکده تابعه", max_length=150)
    TYPE_GROUP = (
        ('community', 'انجمن پژوهشی'),
        ('council', 'شورای پژوهشی'),
        ('center', 'مرکز تحقیقاتی'),
    )
    type_group = models.CharField(max_length=10, verbose_name="نوع مرکز", choices=TYPE_GROUP)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id:
            perv = ResearchGroupProfile.objects.get(id=self.id)
            if perv.photo.name:
                if self.photo.name.split("/")[-1] != perv.photo.name.split("/")[-1]:
                    self.photo = self.compressImage(self.photo)
            else:
                if self.photo.name:
                    self.photo = self.compressImage(self.photo)
        else:
            if self.photo.name:
                self.photo = self.compressImage(self.photo)
        super(ResearchGroupProfile, self).save(*args, **kwargs)

    def compressImage(self, photo):
        imageTemproary = Image.open(photo).convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='JPEG', quality=40)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % photo.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

    # def save(self, *args, **kwargs):
    #     super().save()
    #     if self.photo:
    #         if '\\' in self.photo.name:
    #             self.photo.name = self.photo.name.split('\\')[-1]
    #         elif '/' in self.photo.name:
    #             self.photo.name = self.photo.name.split('/')[-1]
    #     super().save()


class Keyword(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name.__str__()


class ProjectForm(models.Model):
    key_words = models.ManyToManyField(Keyword, verbose_name="کلمات کلیدی")
    persian_title = models.CharField(max_length=256, verbose_name="عنوان فارسی پروژه")
    english_title = models.CharField(max_length=256, verbose_name="عنوان انگلیسی پروژه")
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
    required_method = models.TextField(verbose_name="روش های مورد نیاز", null=True)
    project_phase = models.TextField(verbose_name="مراحل انجام پروژه")
    required_budget = models.IntegerField(verbose_name="بودجه مورد نیاز")
    policy = models.TextField(verbose_name="نکات اخلاقی")
    # predict_profit = models.IntegerField(verbose_name='سود مالی')
    techniques = models.ManyToManyField(Technique, verbose_name="تکنیک های مورد نیاز")

    def __str__(self):
        return self.english_title

    # @property
    # def required_technique(self):
    #     expert_requested = expertModels.ExpertRequestedProject.objects.all().filter(project=self.project).filter(
    #         expert=self.project.expert_accepted).first()
    #     return expert_requested.required_technique.all()


class ResearchProjectForm(models.Model):
    #General Specification
    key_words = models.ManyToManyField(Keyword, verbose_name="کلمات کلیدی")
    persian_title = models.CharField(max_length=256, verbose_name="عنوان فارسی پروژه")
    english_title = models.CharField(max_length=256, verbose_name="عنوان انگلیسی پروژه")
    research_methodology_choice = (
        ("case_series", 'بررسی بیماران'),
        ("cross_sectional", 'مقطعی'),
        ("case_control", 'موردی-شاهدی'),
        ("cohort", 'هم گروهی'),
        ("clinical_trail", 'کارآزمایی بالینی'),
        ("experimental", 'علوم پایه'),
    )
    research_methodology = models.CharField(max_length=15 ,choices=research_methodology_choice, verbose_name="روش تحقیق")

    #Problem Statement
    summary_of_necessity = models.TextField(verbose_name="خلاصه ضرورت اجرا")
    necessity_expression = models.TextField(verbose_name="مشروح بیان پروژه و ضرورت اجرا", null=True, blank=True)
    research_history = models.TextField(verbose_name="سابقه طرح و بررسی متون", null=True, blank=True)

    #Executive Method
    summary_method = models.TextField(verbose_name="خلاصه روش اجرا")
    required_equipment = models.TextField(verbose_name="مشخصات ابزار جمع آوری اطلاعات و نحوه جمع آوری آن", null=True, blank=True)
    sample_count_method = models.TextField(verbose_name="روش محاسبه حجم و تعداد نمونه", null=True, blank=True)
    analyse_method = models.TextField(verbose_name="روش تجزیه و تحلیل داده ها", null=True, blank=True)

    #Goals
    main_goal = models.TextField(verbose_name="اهداف اصلی", null=True, blank=True)
    secondary_goal = models.TextField(verbose_name="اهداف فرعی", null=True, blank=True)
    practical_goal = models.TextField(verbose_name="اهداف کاربردی", null=True, blank=True)
    research_question = models.TextField(verbose_name="سوالات پژوهش", null=True, blank=True)
    reseach_assumptions = models.TextField(verbose_name="فرضیات پژوهش", null=True, blank=True)

    #Morals Considerations
    policy = models.TextField(verbose_name="ملاحظات اخلاقی", null=True, blank=True)
    executive_restrictions = models.TextField(verbose_name="محدودیت های اجرایی و روش کاهش آن ها", null=True, blank=True)
    
    techniques = models.ManyToManyField(Technique, verbose_name="تکنیک های مورد نیاز")

    def __str__(self):
        return self.english_title


def projectFiles(instance, file_name):
    return os.path.join("projects", str(instance), file_name)

class Project(models.Model):
    form = models.OneToOneField(ProjectForm, on_delete=models.CASCADE, verbose_name="فرم پروژه", null=True, blank=True)
    research_project_form = models.OneToOneField(ResearchProjectForm, on_delete=models.CASCADE, verbose_name="فرم پروژه تحقیقاتی", null=True, blank=True)
    code = models.UUIDField(verbose_name="کد پروژه", default=uuid.uuid4, unique=True)
    date_submitted_by_industry = models.DateField(verbose_name="تاریخ ثبت پرژه توسط صنعت", auto_now_add=True)
    date_project_started = models.DateField(verbose_name="تاریخ شروع پروژه", null=True, blank=True)
    researcherRequestDeadline = models.DateField(verbose_name="مهلت درخواست پژوهشگر", auto_now=False, auto_now_add=False, null=True, blank=True)
    finish_date_suggested = models.DateField(verbose_name="تاریخ پیشنهادی اتمام پروژه", auto_now=False, auto_now_add=False, null=True, blank=True)
    date_finished = models.DateField(verbose_name="تاریخ اتمام پروژه", null=True, blank=True)
    researcher_applied = models.ManyToManyField('researcher.ResearcherUser', through='researcher.RequestedProject',
                                                verbose_name="پژوهشگران درخواست داده",
                                                related_name="researchers_applied", blank=True)
    researcher_accepted = models.ManyToManyField('researcher.ResearcherUser', verbose_name="پژوهشگران پذبرفته شده",
                                                 related_name="researchers_accepted", blank=True)
    researcher_banned = models.ManyToManyField('researcher.ResearcherUser', verbose_name="پژوهشگران رد شده",
                                               related_name="researchers_banned", blank=True)
    expert_applied = models.ManyToManyField('expert.ExpertUser', through='expert.ExpertRequestedProject',
                                            verbose_name="اساتید درخواست داده",
                                            related_name="experts_applied", blank=True)
    expert_accepted = models.ManyToManyField('expert.ExpertUser', verbose_name="استاد پذیرفته شده",
                                        related_name="expert_accepted", blank=True)
    expert_suggested = models.ManyToManyField("expert.ExpertUser", verbose_name="استاد پیشنهادی",
                                        related_name="expert_suggested", blank=True)
    expert_messaged = models.ManyToManyField('expert.ExpertUser', blank=True, related_name="expert_messaged",
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
        (1, 'در حال انتظار'),
        (2, 'فعال'),
        (3, 'معلق'),
        (4, 'انجام شد'),
    )
    status = models.IntegerField(choices=PROJECT_STATUS_CHOICES, verbose_name='وضعیت پروژه', default=0, blank=True)
    expert_banned = models.ManyToManyField("expert.ExpertUser", verbose_name="اساتید رد شده",
                                           related_name="expert_banned", blank=True)
    executive_info = models.TextField(verbose_name="توضیحات اجرایی", null=True, blank=True)
    reseacherRequestAbility = models.BooleanField(verbose_name="قابلیت درخواست پژوهشگر", default=False, null=True)
    telegram_group = models.CharField(verbose_name="لینک تلگرام", max_length=256, null=True, blank=True)
    end_note = models.FileField(verbose_name="فایل endNote", upload_to=projectFiles, max_length=128, null=True, blank=True)
    proposal = models.FileField(verbose_name="فایل پروپوزال", upload_to=projectFiles, max_length=128, null=True, blank=True)

    class Meta:
        ordering = ['-date_submitted_by_industry']

    def __str__(self):
        try:
            return self.form.english_title
        except:
            return self.research_project_form.english_title

    def get_comments(self):
        project_comments = Comment.objects.all().filter(project=self).reverse()
        return project_comments

    @property
    def firstExpert(self):
        return self.expert_accepted.all().first()

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
        comment = self.get_comments()
        expert_unseen = comment.filter(sender_type='expert').filter(status='unseen').filter(
            industry_user=self.industry_creator).count()
        system_unseen = comment.filter(sender_type='system').filter(status='unseen').filter(
            industry_user=self.industry_creator).count()
        return expert_unseen + system_unseen

    @property
    def project_form(self):
        if self.form is not None:
            return self.form
        else:
            return self.research_project_form

    @property
    def involved_user(self):
        expertUsers = []
        for expert in self.expert_accepted.all():
            expertInfo = {
                "username": expert.userId,
                "fullname": expert.expertform.fullname
            }
            if expert.expertform.photo:
                expertInfo["photo"] = expert.expertform.photo.url
            expertUsers.append(expertInfo)
        
        researcherUsers = []
        for researcher in self.researcher_accepted.all():
            researcherInfo = {
                "username": researcher.userId,
                "fullname": researcher.researcherprofile.fullname
            }
            if researcher.researcherprofile.photo:
                researcherInfo["photo"] = researcher.researcherprofile.photo.url
            researcherUsers.append(researcherInfo)

        industryInfo = {
            "username" : self.industry_creator.userId,
            "fullname" : self.industry_creator.profile.name
        }
        if self.industry_creator.profile.photo:
            industryInfo['photo'] = self.industry_creator.profile.photo.url
        data = {
            "expertUsers": expertUsers,
            "researcherUsers": researcherUsers,
            "industryUser": industryInfo
        }
        return data

    def get_involved_user(self, userId):
        try:
            return self.researcher_accepted.get(userId=userId), "researcher"
        except:
            try:
                return self.expert_accepted.get(userId=userId), "expert"
            except:
                if self.industry_creator.userId == userId:
                    return self.industry_creator, "industry"
                else:
                    return None, None
                    

    def is_date_valid(self):
        return True
        # if self.date_project_started is not None and self.date_finished is not None and \
        #         self.date_phase_two_deadline is not None and self.finish_date_suggested is not None and \
        #         self.date_start:
        #     return True
        # return False


def upload_comment(instance, file_name):
    return os.path.join(instance.project.__str__(), file_name)
    # if instance.researcher_user is None:
    #     if instance.sender_type == "expert":
    #         return os.path.join(instance.project.__str__(), "Comments", "Expert&Industry", "Expert", file_name)
    #     else:
    #         return os.path.join(instance.project.__str__(), "Comments", "Expert&Industry", "Industry", file_name)
    # else:
    #     if instance.sender_type == "expert":
    #         return os.path.join(instance.project.__str__(), "Comments", "Expert&Researcher", "Expert", file_name)
    #     else:
    #         print("==========-----")
    #         return os.path.join(instance.project.__str__(), "Comments", "Expert&Researcher", "Reseacher", file_name)


class Comment(models.Model):
    description = models.TextField(verbose_name="متن")
    SENDER = (
        ("expert", 'استاد'),
        ("industry", 'صنعت'),
        ("researcher", 'پژوهشگر'),
        ("system", 'سیستم'),
    )
    replied_text = models.CharField(max_length=150, blank=True, null=True)
    sender_type = models.CharField(max_length=10, choices=SENDER)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    industry_user = models.ForeignKey(IndustryUser, on_delete=models.SET_NULL, null=True, blank=True)
    expert_user = models.ForeignKey('expert.ExpertUser', on_delete=models.SET_NULL, null=True, blank=True)
    researcher_user = models.ForeignKey(ResearcherUser, on_delete=models.SET_NULL, null=True, blank=True)

    attachment = models.FileField(upload_to=upload_comment, blank=True, null=True)
    date_submitted = models.DateField(auto_now_add=True, verbose_name="تاریخ ثبت")
    STATUS = (
        ('seen', 'seen'),
        ('unseen', 'unseen'),
    )
    status = models.CharField(max_length=6, choices=STATUS, null=True)

    def __str__(self):
        return self.sender_type + " - " + str(self.project)


class ProjectHistory(models.Model):
    english_title = models.CharField(max_length=128)
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
        return "history of " + self.english_title


class ExpertEvaluateIndustry(models.Model):
    industry = models.ForeignKey(IndustryUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    expert = models.ForeignKey('expert.ExpertUser', on_delete=models.CASCADE, blank=True, null=True)
    phase = models.IntegerField(verbose_name="فاز شماره : ", null=True)
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
