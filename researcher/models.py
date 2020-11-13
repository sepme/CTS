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

# for Compress the photo
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def profileUpload(instance, filename):
    return os.path.join('Researcher Profile', instance.researcher_user.user.username, filename)
    # ext = filename.split('.')[-1]
    # filename = '{}.{}'.format('profile', ext)

    # return os.path.join('unique', instance.researcher_user.user.username, filename)


def get_answerFile_path(instance, filename):
    full_filename = "answer-" + instance.researcher.user.username + "-" + filename
    # folder_name = instance.research_question.expert.user.username + '-' + instance.research_question.question_title
    folder_name = str(instance.research_question.pk)
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

def addResearchTechniques(researcher, evaluator):
    searching_technique = Technique.objects.get(technique_title='Searching')
    techniqueInstance = TechniqueInstance.objects.get_or_create(researcher=researcher
                                                        ,technique=searching_technique
                                                        ,level="A"
                                                        ,evaluator=evaluator)
    Ref_technique = Technique.objects.get(technique_title='Reference Management (Endnote/Mendeley/...)')
    techniqueInstance = TechniqueInstance.objects.get_or_create(researcher=researcher
                                                        ,technique=Ref_technique
                                                        ,level="A"
                                                        ,evaluator=evaluator)
    return

class ResearcherUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    userId = models.CharField(verbose_name="ID کاربر", max_length=50, blank=True, null=True)
    points = models.FloatField(default=0.0, verbose_name='امتیاز')
    unique = models.UUIDField(unique=True, default=uuid.uuid4)
    chat_id = models.CharField(verbose_name="آیدی چت", max_length=50, null=True, blank=True)

    class Meta:
        permissions = (
            ('be_researcher', 'Be Researcher'),
            ('is_active', 'is active'),
        )

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse("researcher:index"))

    @property
    def score(self):
        return self.points * 23

    def get_name(self):
        return self.researcherprofile.fullname


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
    inactivate_duration = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True,
                                               verbose_name="غیرفعال تا تاریخ")

    # inactivate_duration_temp = models.DateField(default='0001-01-01' , blank=True, null=True)

    @property
    def is_deactivated(self):
        today = datetime.datetime.now(datetime.timezone.utc)
        if self.inactivate_duration:
            if today > self.inactivate_duration:
                return False
            else:
                return True
        return False

    @property
    def remainingTime(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = self.inactivate_duration - now
        remaining = {}
        remaining['day'] = delta.days
        remaining['hour'] = delta.seconds // 3600
        remaining['minute'] = (delta.seconds % 3600) // 60
        remaining['second'] = delta.seconds % 60
        return remaining

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
    photo = models.ImageField(upload_to=profileUpload, max_length=256, blank=True, null=True)
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
    awards = models.TextField(verbose_name="افتخارات",max_length=1000, null=True, blank=True)

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
    resume = models.FileField(verbose_name="رزومه دانشجو", upload_to=profileUpload, max_length=511,
                              null=True, blank=True)

    def __str__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        if self.id:
            perv = ResearcherProfile.objects.get(id=self.id)
            if perv.photo.name:
                if self.photo.name.split("/")[-1] != perv.photo.name.split("/")[-1]:
                    self.photo = self.compressImage(self.photo)
            else:
                if self.photo.name:
                    self.photo = self.compressImage(self.photo)
        else:
            if self.photo.name:
                self.photo = self.compressImage(self.photo)
        super(ResearcherProfile, self).save(*args, **kwargs)

    def compressImage(self, photo):
        imageTemproary = Image.open(photo).convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='JPEG', quality=40)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % photo.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

    def get_resume_name(self):
        try:
            return os.path.basename(self.resume.name)[:os.path.basename(self.resume.name).rfind(".")]
        except:
            return ""

    def get_resume_ext(self):
        try:
            return os.path.basename(self.resume.name)[os.path.basename(self.resume.name).rfind(".") + 1:]
        except:
            return ""

    def get_resume_icon(self):
        try:
            icon = "unknown"
            ext = self.get_resume_ext()
            if ext.lower() == "pdf":
                icon = "pdf"
            elif ext.lower() == "doc":
                icon = "doc"
            elif ext.lower() == "gif":
                icon = "gif"
            elif ext.lower() == "jpg":
                icon = "jpg"
            elif ext.lower() == "png":
                icon = "png"
            elif ext.lower() == "ppt":
                icon = "ppt"
            elif ext.lower() == "txt":
                icon = "txt"
            elif ext.lower() == "wmv":
                icon = "wmv"
            elif ext.lower() == "zip":
                icon = "zip"
            return icon
        except:
            return "unknown"


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
    presenter = models.CharField(max_length=256, verbose_name="نام مجری")
    responsible = models.CharField(max_length=256, verbose_name="مسئول اجرا / همکار")
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
    project_title = models.CharField(max_length=127, verbose_name="عنوان پروژه")
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
    tutorial_link = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.technique_title

    @staticmethod
    def get_technique_list():
        technique_list = {
            "Molecular Biology": [technique.technique_title for technique in
                                  Technique.objects.filter(technique_type='molecular_biology')],
            "Immunology": [technique.technique_title for technique in
                           Technique.objects.filter(technique_type='immunology')],
            "Imaging": [technique.technique_title for technique in Technique.objects.filter(technique_type='imaging')],
            "Histology": [technique.technique_title for technique in
                          Technique.objects.filter(technique_type='histology')],
            "General Lab": [technique.technique_title for technique in
                            Technique.objects.filter(technique_type='general_lab')],
            "Animal Lab": [technique.technique_title for technique in
                           Technique.objects.filter(technique_type='animal_lab')],
            "Lab Safety": [technique.technique_title for technique in
                           Technique.objects.filter(technique_type='lab_safety')],
            "Biochemistry": [technique.technique_title for technique in
                             Technique.objects.filter(technique_type='biochemistry')],
            "Cellular Biology": [technique.technique_title for technique in
                                 Technique.objects.filter(technique_type='cellular_biology')],
            "Research Methodology": [technique.technique_title for technique in
                                     Technique.objects.filter(technique_type='research_methodology')],
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
        if days_passed == 0:
            return "امروز"
        total_passed = ""
        if days_passed > 364:
            total_passed = persianNumber.convert(str(days_passed // 365)) + " سال "
        days_passed = days_passed % 365
        if days_passed > 30:
            if total_passed == "":
                total_passed = persianNumber.convert(str(days_passed // 30)) + " ماه "
            else:
                total_passed += " و " + persianNumber.convert(str(days_passed // 30)) + " ماه "
        days_passed = days_passed % 30
        if total_passed == "":
            total_passed = persianNumber.convert(str(days_passed)) + " روز "
        else:
            total_passed += " و " + persianNumber.convert(str(days_passed)) + " روز "
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

    STATUS = (
        ('unseen', "unseen"),
        ('pending', 'pending'),
        ('accepted', "accepted"),
        ('rejected', 'rejected'),
        ('removed', 'removed'),
    )
    status = models.CharField(verbose_name="وضعیت درخواست", max_length=10, choices=STATUS, default='unseen')

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
    is_correct = models.CharField(max_length=10, verbose_name="تایید استاد", choices=(
        ('not_seen', 'بررسی نشده'),
        ('correct', 'صحیح'),
        ('wrong', 'غلط'),
    ), default='not_seen')

    def __str__(self):
        return str(self.research_question) + ' - ' + self.researcher.user.username

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id:
            perv = ResearchQuestionInstance.objects.get(id=self.id)
            if perv.is_correct == "not_seen" and self.is_correct == "correct":
                message = Message.objects.filter(title="تایید سوال پژوهشی").first()
                if message is None:
                    context = """با سلام،
پژوهشگر گرامی، پاسخ سوال پژوهشی شما پذیرفته شد.
به این ترتیب، پیوستن شما به مجموعه پژوهشگران «چمران‌تیم» را تبریک می‌گوییم و امیدواریم شاهد پیشرفت شما در زمینه پژوهش باشیم.
از این پس می‌توانید از طریق قسمت «پروژه‌ها» برای شرکت در پروژه‌های تعریف‌شده توسط مجموعه‌های پژوهشی، درخواست ارسال کنید. 
البته در نظر داشته باشید که برای شرکت در هر پروژه‌ای، لازم است مهارت‌های پژوهشی آن پروژه را قبلا کسب کرده باشید. به همین خاطر، توصیه می‌کنیم به قسمت «مهارت‌های پژوهشی» حساب کاربری‌تان هم سر بزنید و با افزایش تعداد مهارت‌های‌تان، شانس خود را برای شرکت در پروژه‌ها افزایش دهید.
همچنین، با تکمیل یا بارگذاری رزومه علمی‌تان از طریق قسمت «اطلاعات کاربری»، می‌توانید توانمندی‌های خود را در هنگام انتخاب شدن‌تان توسط استاد و یا مجموعه پژوهشی، نشان دهید.
با آرزوی موفقیت، 
چمران‌تیم"""
                    message = Message.objects.create(title="تایید سوال پژوهشی",
                                                     text=context,
                                                     type=0)
                message.receiver.add(self.researcher.user)
                message.save()
                status = self.researcher.status
                status.status = "free"
                status.save()
                addResearchTechniques(self.researcher, self.research_question.expert.expertform.__str__())
            elif perv.is_correct == "not_seen" and self.is_correct == "wrong":                
                title = "رد سوال پژوهشی"
                message = Message.objects.filter(title=title).first()
                if message is None:
                    text = """با سلام،
    پژوهشگر گرامی، متاسفانه پاسخ شما به سوال پژوهشی (در مهلت یک هفته‌ای ارسال نشد / به دلیل نداشتن کیفیت مناسب، مورد قبول واقع نشد).
    علی‌رغم میل درونی، حساب کاربری شما به مدت دو هفته به حالت تعلیق در خواهد آمد و پس از آن، مجددا می‌توانید در یک سوال پژوهشی شرکت نمایید.
    امیدواریم دو هفته‌ی دیگر هم شما را ببینیم.
    در ضمن، در صورتی که فکر می‌کنید این پیام به اشتباه ارسال شده است، می‌توانید مراتب اعتراض خود را از طریق شماره تلفن ۰۹۱۰۲۱۴۳۴۵۱ و یا فرم ارسال گزارش (با کلیک بر روی تصویر علامت تعجب در گوشه بالا سمت چپ صفحه نمایش) ارسال فرمایید.
    با آرزوی موفقیت،
    چمران‌تیم"""
                    messageType = 1
                    message = Message.objects.create(title=title,
                                                     text=text,
                                                     type=messageType)
                message.receiver.add(answer.researcher.user)
                message.save()
                status = self.researcher.status
                researcher = self.researcher
                status.status = 'deactivated'
                inactivate_date = datetime.date.today() + datetime.timedelta(days=30)        
                status.inactivate_duration = inactivate_date
                status.save()
                ctype = ContentType.objects.get_for_model(ResearcherUser)
                permission = Permission.objects.get(content_type=ctype, codename='is_active')
                researcher.user.user_permissions.remove(permission)
                researcher.user.save()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
