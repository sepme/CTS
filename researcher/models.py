from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse, HttpResponseRedirect
from django.utils.timezone import now
import os
import datetime
import uuid
from . import persianNumber
from chamran_admin.models import Message

#for Compress the photo
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def profileUpload(instance, filename):
    return os.path.join('Researcher Profile' , instance.researcher_user.user.username ,filename)
    # ext = filename.split('.')[-1]
    # filename = '{}.{}'.format('profile', ext)

    # return os.path.join('unique', instance.researcher_user.user.username, filename)



def get_answerFile_path(instance, filename):
    full_filename = "answer-" + instance.researcher.user.username + "-" + filename
    folder_name = instance.research_question.expert.user.username + '-' + instance.research_question.question_title
    path = os.path.join('Research Question', folder_name)
    return os.path.join(path, full_filename)


def get_resumeFile_path(instance, filename):
    ext = filename.split('.')[-1]
    try:
        filename = '{}.{}'.format("resume-" +
                                  instance.researcher.user.username + "-" +
                                  instance.technique.technique_title + "-" +
                                  "-".join(filename.split('.')[:-1]), ext)
        folder_name = str(instance.researcher)
    except:
        filename = '{}.{}'.format("new-resume-" +
                                  instance.technique_instance.researcher.user.username + "-" +
                                  instance.technique_instance.technique.technique_title + "-" +
                                  "-".join(filename.split('.')[:-1]), ext)
        folder_name = str(instance.technique_instance.researcher)
    return os.path.join('resume', folder_name, filename)


class ResearcherUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    points = models.FloatField(default=0.0, verbose_name='امتیاز')
    unique = models.UUIDField(unique=True, default=uuid.uuid4)

    class Meta:
        permissions = (
            ('be_researcher' ,'Be Researcher'),
            ('is_active' ,'is active'),
            )
    
    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse("researcher:index"))

    @property
    def score(self):
        return self.points*23

class Status(models.Model):
    researcher_user = models.OneToOneField("ResearcherUser", on_delete=models.CASCADE, blank=True, null=True)
    STATUS = (
        ('signed_up', "فرم های مورد نیاز تکمیل نشده است. "),
        ('not_answered', "به سوال پژوهشی پاسخ نداده است."),
        ('wait_for_result', "منتظر جواب ادمین"),
        ('free', "فعال - بدون پروژه"),
        ('waiting', "فعال - در حال انتظار پروژه"),
        ('involved', "فعال - درگیر پروژه"),
        ('deactivated', "غیر فعال - تویط مدیر سایت غیر فعال شده است."),
    )
    status = models.CharField(max_length=15, choices=STATUS, default='signed_up')
    inactivate_duration = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    inactivate_duration_temp = models.DateField(verbose_name="غیرفعال تا تاریخ",default='0001-01-01' , blank=True, null=True)

    @property
    def check_activity_status(self):
        today = datetime.datetime.today().date()
        if  today > self.inactivate_duration_temp:
            return True
        return False

    def __str__(self):
        return '{user} - {status}'.format(user=self.researcher_user, status=self.status)

class MembershipFee(models.Model):
    researcher_user = models.OneToOneField('ResearcherUser', verbose_name="حق عضویت", on_delete=models.CASCADE,
                                           blank=True, null=True)
    fee = models.IntegerField(verbose_name='هزینه')
    start = models.DateField(auto_now=False, auto_now_add=False, verbose_name="اولین پرداخت")
    rePay = models.DateField(auto_now=False, auto_now_add=False, verbose_name="آخرین پرداخت")

    def __str__(self):
        return str(self.fee)

class ResearcherProfile(models.Model):
    researcher_user = models.OneToOneField("ResearcherUser", verbose_name="مشخصات فردی",
                                           on_delete=models.CASCADE, blank=True, null=True)
    fullname = models.CharField(max_length=300, verbose_name="نام و نام خانوادگی")
    photo = models.ImageField(upload_to=profileUpload, max_length=255, blank=True, null=True)
    birth_year = models.DateField(auto_now=False, auto_now_add=False, verbose_name="سال تولد", null=True, blank=True)
    major = models.CharField(max_length=300, verbose_name="رشته تحصیلی")
    national_code = models.CharField(max_length=10, verbose_name="کد ملی")

    GRADE_CHOICE = (
        (1, 'کارشناسی'),
        (2, 'کارشناسی ارشد'),
        (3, 'دکتری'),
        (4, 'دکتری حرفه‌ای'),
    )
    grade = models.IntegerField(choices=GRADE_CHOICE, verbose_name="آخرین مدرک تحصیلی")
    university = models.CharField(max_length=300, verbose_name="دانشگاه محل تحصیل")
    entry_year = models.CharField(max_length=6, verbose_name="سال ورود")
    address = models.TextField(verbose_name="آدرس محل سکونت")
    home_number = models.CharField(max_length=50, verbose_name="تلفن منزل")
    phone_number = models.CharField(max_length=50, verbose_name="تلفن همراه")
    email = models.EmailField(max_length=254, verbose_name="پست الکترونیکی")
    student_number = models.CharField(max_length=10, verbose_name="شماره دانشجویی")

    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    INT_CHOICE = (
        (one, '1'),
        (two, '2'),
        (three, '3'),
        (four, '4'),
        (five, '5'),
    )

    team_work = models.IntegerField(choices=INT_CHOICE, verbose_name="روحیه کار تیمی",
                                    blank=True, null=True)
    creative_thinking = models.IntegerField(choices=INT_CHOICE, verbose_name="تفکر خلاقانه", blank=True, null=True)

    interest_in_major = models.IntegerField(choices=INT_CHOICE, verbose_name="علاقه به رشته تحصیلی",
                                            blank=True, null=True)
    motivation = models.IntegerField(choices=INT_CHOICE, verbose_name="انگیزه داشتن برای انجام پروژه",
                                     blank=True, null=True)
    sacrifice = models.IntegerField(choices=INT_CHOICE, verbose_name="تعهد داشتن و از خود گذشتگی",
                                    blank=True, null=True)
    diligence = models.IntegerField(choices=INT_CHOICE, verbose_name="پشتکار", blank=True, null=True)
    interest_in_learn = models.IntegerField(choices=INT_CHOICE, verbose_name="علاقه به یادگیری",
                                            blank=True, null=True)
    punctuality = models.IntegerField(choices=INT_CHOICE, verbose_name="وقت­شناسی", blank=True, null=True)
    data_collection = models.IntegerField(choices=INT_CHOICE, verbose_name="جمع­ آوری داده­ ها",
                                          blank=True, null=True)
    project_knowledge = models.IntegerField(choices=INT_CHOICE, verbose_name="آگاهی از اصول انجام پروژه"
                                            , blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        if self.id:
            perv = ResearcherProfile.objects.get(id=self.id)
            if perv.photo.name.split("/")[-1] != self.photo.name.split("/")[-1]:
                self.photo = self.compressImage(self.photo)
        else:
            self.photo = self.compressImage(self.photo)
        super(ResearcherProfile, self).save(*args, **kwargs)

    def compressImage(self,photo):
        imageTemproary = Image.open(photo).convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imageTemproary.save(outputIoStream , format='JPEG', quality=40)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % photo.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

class ScientificRecord(models.Model):
    researcherProfile = models.ForeignKey("ResearcherProfile", verbose_name="سوابق علمی", on_delete=models.CASCADE)

    grade = models.CharField(max_length=300, verbose_name="مقطع تحصیلی")
    major = models.CharField(max_length=300, verbose_name="رشته تحصیلی")
    university = models.CharField(max_length=300, verbose_name="دانشگاه")
    place = models.CharField(max_length=300, verbose_name="شهر محل تحصیل")
    graduated_year = models.CharField(max_length=15, verbose_name="سال اخذ مدرک")

    def __str__(self):
        return self.grade

class ExecutiveRecord(models.Model):
    researcherProfile = models.ForeignKey("ResearcherProfile", verbose_name="سوابق اجرایی", on_delete=models.CASCADE)

    post = models.CharField(max_length=300, verbose_name="سمت")
    start = models.CharField(max_length=30, verbose_name="از تاریخ")
    end = models.CharField(max_length=30, verbose_name="تا تاریخ")
    place = models.CharField(max_length=300, verbose_name="نام مجموعه")
    city = models.CharField(max_length=300, verbose_name="شهر")

    def __str__(self):
        return self.post

class StudiousRecord(models.Model):
    researcherProfile = models.ForeignKey("ResearcherProfile", verbose_name="سوابق پژوهشی", on_delete=models.CASCADE)

    title = models.CharField(max_length=300, verbose_name="عنوان طرح پژوهشی")
    presenter = models.CharField(max_length=50, verbose_name="نام مجری")
    responsible = models.CharField(max_length=50, verbose_name="مسئول اجرا / همکار")
    STATUS_CHOICE = (
        (1, 'در دست اجرا'),
        (2, 'خاتمه یافته'),
        (3, 'متوقف'),
    )
    status = models.IntegerField(choices=STATUS_CHOICE, verbose_name="وضعیت طرح پژوهشی")

    def __str__(self):
        return self.title

class ResearcherHistory(models.Model):
    researcher_profile = models.ForeignKey("ResearcherProfile", verbose_name="تاریخچه", on_delete=models.CASCADE)

    title = models.CharField(max_length=300, verbose_name="عنوان پروژه")
    start = models.DateField(auto_now=False, auto_now_add=False, verbose_name="تاریخ شروع")
    end = models.DateField(auto_now=False, auto_now_add=False, verbose_name="تاریخ پایان")
    STATUS_CHOICE = (
        ('completed', 'completed'),
        ('stopped', 'stopped'),
    )
    status = models.CharField(max_length=9, choices=STATUS_CHOICE, verbose_name="وضعیت")
    point = models.FloatField(verbose_name='امتیاز')
    income = models.IntegerField(verbose_name='درآمد')
    involve_tech = models.ManyToManyField('Technique', verbose_name="تکنیک های استفاده شده")

    def __str__(self):
        return "history of " + self.researcher_profile.fullname

class ResearcherEvaluation(models.Model):
    researcher = models.ForeignKey('ResearcherUser', on_delete=models.CASCADE)
    evaluator = models.ForeignKey("expert.ExpertUser", on_delete=models.CASCADE, null=True, blank=True)
    project_title = models.CharField(max_length=128, verbose_name="عنوان پروژه")
    phase = models.IntegerField(verbose_name="فاز شماره : ")

    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    INT_CHOICE = (
        (one, '1'),
        (two, '2'),
        (three, '3'),
        (four, '4'),
        (five, '5'),
    )

    time_assign = models.IntegerField(choices=INT_CHOICE,
                                      verbose_name="به چه میزان دانشجو مطابق زمان از پیش اعلام شده در هفته، برای کار زمان تخصیص داد؟ ")
    flexibility = models.IntegerField(choices=INT_CHOICE,
                                      verbose_name="میزان رضایت شما از انعطاف زمانبندی ارائه شده توسط دانشجو، چقدر است؟")
    mastery_techniq = models.IntegerField(choices=INT_CHOICE,
                                          verbose_name="دانشجو تسلط بر تکنیک های اعلام شده چه میزان بوده است؟ ")
    verification_records = models.IntegerField(choices=INT_CHOICE,
                                               verbose_name="صحت سوابق و مهارتهای اعلام شده توسط دانشجو چقدر بوده است؟")
    professional = models.IntegerField(choices=INT_CHOICE,
                                       verbose_name="میزان رضایت شما از رفتار حرفه ای دانشجو، چه اندازه است؟")
    cooperation = models.IntegerField(choices=INT_CHOICE,
                                      verbose_name="دانشجو چه میزان همکاری سازنده با سایر اعضای تیم داشته است؟(کمک به ارتقای سطح دانش علمی و عملی گروه)")
    satisfaction = models.IntegerField(choices=INT_CHOICE,
                                       verbose_name="میزان رضایت شما از دانشجو در ازای ارائه نتایج عملکرد به شما چقدر بوده است ؟")
    total_satisfaction = models.IntegerField(choices=INT_CHOICE,
                                             verbose_name="میزان رضایت کلی شما از دانشجو چه اندازه است؟")
    next_cooperation = models.IntegerField(choices=INT_CHOICE,
                                           verbose_name="چقدر تمایل دارید در همکاری های بعدی با دانشجو همکاری کنید؟")
    chamran_team = models.IntegerField(choices=INT_CHOICE,
                                       verbose_name="میزان رضایت شما از عملکرد چمران تیم در این پروژه چقدر بوده است؟")

    def average(self):
        sum = 0.0
        sum = self.time_assign + self.flexibility + self.mastery_techniq + self.verification_records
        sum = sum + self.professional + self.cooperation + self.satisfaction + self.total_satisfaction
        sum = sum + self.next_cooperation + self.chamran_team
        ava = float(sum / 10)
        return ava

class Technique(models.Model):
    TYPE = (
        ('molecular_biology', 'Molecular Biology'),
        ('immunology', 'Immunology'),
        ('imaging', 'Imaging'),
        ('histology', 'Histology'),
        ('general_lab', 'General Lab'),
        ('animal_lab', 'Animal Lab'),
        ('lab_safety', 'Lab Safety'),
        ('biochemistry', 'Biochemistry'),
        ('cellular_biology', 'Cellular Biology'),
        ('research_methodology', 'Research Methodology'),
    )

    technique_type = models.CharField(max_length=30, choices=TYPE, blank=True)
    technique_title = models.CharField(max_length=300)
    tutorial_link = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.technique_title

    @staticmethod
    def get_technique_list():
        technique_list = {
            "molecular_biology" : [technique.technique_title for technique in Technique.objects.filter(technique_type='molecular_biology')],
            "immunology" : [technique.technique_title for technique in Technique.objects.filter(technique_type='immunology')],
            "imaging" : [technique.technique_title for technique in Technique.objects.filter(technique_type='imaging')],
            "histology" : [technique.technique_title for technique in Technique.objects.filter(technique_type='histology')],
            "general_lab" : [technique.technique_title for technique in Technique.objects.filter(technique_type='general_lab')],
            "animal_lab" : [technique.technique_title for technique in Technique.objects.filter(technique_type='animal_lab')],"lab_safety" : [technique.technique_title for technique in Technique.objects.filter(technique_type='lab_safety')],
            "biochemistry" : [technique.technique_title for technique in Technique.objects.filter(technique_type='biochemistry')],
            "cellular_biology" : [technique.technique_title for technique in Technique.objects.filter(technique_type='cellular_biology')],
            "research_methodology" : [technique.technique_title for technique in Technique.objects.filter(technique_type='research_methodology')],
            }
        return technique_list


class TechniqueInstance(models.Model):
    researcher = models.ForeignKey("ResearcherUser", on_delete=models.CASCADE)
    technique = models.ForeignKey("Technique", verbose_name="مهارت", on_delete=models.CASCADE, null=True, blank=True)
    TECH_GRADE = (
        ('A', 'به صورت عملی در پروژه انجام داده است.'),
        ('B', 'به صورت عملی در کارگاه آموزش دیده است.'),
        ('C', 'به صورت تئوری آموزش دیده است.'),
    )
    level = models.CharField(max_length=1, choices=TECH_GRADE, verbose_name='سطح مهارت', blank=True, null=True)
    resume = models.FileField(upload_to=get_resumeFile_path, max_length=100, null=True, blank=True)
    evaluator = models.CharField(max_length=300, verbose_name='ارزیابی کننده', blank=True)
    evaluat_date = models.DateField(verbose_name="زمان نمره گرفتن", auto_now=True, null=True)

    def is_validated(self):
        if self.level == 'A' or self.level == 'B' or self.level == 'C':
            return True
        return False

    @property
    def date_last(self):
        days_passed = (datetime.datetime.today().date() - self.evaluat_date).days
        total_passed = ""
        if days_passed > 364:
            total_passed = persianNumber.convert(str(days_passed // 365)) + " سال "
        days_passed = days_passed % 365
        if days_passed > 30:
            if total_passed == "" :
                total_passed = persianNumber.convert(str(days_passed // 30)) + " ماه "
            else:
                total_passed += " و " + persianNumber.convert(str(days_passed // 30)) + " ماه "
        days_passed = days_passed % 30
        if total_passed == "" :
            total_passed = persianNumber.convert(str(days_passed)) + " روز "
        else:
            total_passed += " و " + persianNumber.convert(str(days_passed)) + " روز "
        if total_passed == "":
            total_passed = "امروز"
        else:
            total_passed += " پیش"
        return total_passed

    def __str__(self):
        return str(self.researcher) + " - " + str(self.technique)


class TechniqueReview(models.Model):
    technique_instance = models.ForeignKey(TechniqueInstance, verbose_name="تکنیک", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="توضیحات")
    resume = models.FileField(upload_to=get_resumeFile_path, max_length=100, null=True)
    method = models.CharField(max_length=30)
    result = models.CharField(max_length=1, null=True)

    def __str__(self):
        return str(self.technique_instance)


class RequestedProject(models.Model):
    researcher = models.ForeignKey("researcher.ResearcherUser", on_delete=models.CASCADE)
    project = models.ForeignKey("industry.Project", on_delete=models.CASCADE, null=True, blank=True)
    date_requested = models.DateField(default=now, verbose_name='تاریخ درخواست')
    least_hours_offered = models.IntegerField(default=0, verbose_name='حداقل مدت زمانی پیشنهادی در هفته')
    most_hours_offered = models.IntegerField(default=0, verbose_name='حداکثر مدت زمانی پیشنهادی در هفته')
    def __str__(self):
        return str(self.project) + " - " + str(self.date_requested)

class ResearchQuestionInstance(models.Model):
    research_question = models.ForeignKey('expert.ResearchQuestion', on_delete=models.CASCADE,
                                          verbose_name="سوال پژوهشی")
    researcher = models.ForeignKey(ResearcherUser, on_delete=models.CASCADE, verbose_name="پژوهشگر",
                                   blank=True, null=True)
    hand_out_date = models.DateTimeField(verbose_name="تاریخ واگذاری", default=now)
    answer = models.FileField(upload_to=get_answerFile_path, verbose_name="پاسخ", null=True, blank=True)
    is_answered = models.BooleanField(verbose_name="پاسخ داده شده", default=False)
    is_correct = models.CharField(max_length=10, verbose_name="تایید استاد", choices={
        ('not_seen', 'بررسی نشده'),
        ('correct', 'صحیح'),
        ('wrong', 'غلط'),
    }, default='not_seen')

    def __str__(self):
        return str(self.research_question) + ' - ' + self.researcher.user.username

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id:
            perv = ResearchQuestionInstance.objects.get(id=self.id)
            if perv.is_correct == "not_seen" and self.is_correct == "correct":
                message = Message.objects.get(id=2)
                message.receiver.add(self.researcher.user)
                message.save()
                status = self.researcher.status
                status.status = "free"
                status.save()
                user = self.researcher.user
                ctype = ContentType.objects.get_for_model(ResearcherUser)
                permission = Permission.objects.get(content_type=ctype, codename='is_active')
                user.user_permissions.add(permission)
                user.save()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)