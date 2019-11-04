from django.db import models
from django.contrib.auth.models import User
import os
from django.shortcuts import reverse, HttpResponseRedirect
import uuid
from industry.models import Keyword

def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format('profile', ext)

    return os.path.join('unique', instance.expert_user.user.username, filename)

def get_attachment_path(instance, filename):
    return os.path.join('Research Question', instance.expert.user.username+'-'+instance.question_title, filename)


class ExpertUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر استاد")
    expert_point = models.IntegerField(verbose_name="امتیاز استاد", default=0.0)
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
        return HttpResponseRedirect(reverse("expert:index"))


class EqTest(models.Model):
    INT_CHOICE = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    team_work = models.IntegerField(choices=INT_CHOICE, verbose_name="روحیه کار تیمی")
    innovation = models.IntegerField(choices=INT_CHOICE, verbose_name="تفکر خلاقانه")
    devotion = models.IntegerField(choices=INT_CHOICE, verbose_name="تعهد و ازخوگذشتگی")
    productive_research = models.IntegerField(choices=INT_CHOICE, verbose_name="پژوهش محصولمحور")
    national_commitment = models.IntegerField(choices=INT_CHOICE, verbose_name="تعهد ملی")
    collecting_information = models.IntegerField(choices=INT_CHOICE, verbose_name="جمع اوری داده")
    business_thinking = models.IntegerField(choices=INT_CHOICE, verbose_name="روحیه بیزینسی")
    risk_averse = models.IntegerField(choices=INT_CHOICE, verbose_name="ریسک پذیری")


class ExpertForm(models.Model):
    expert_user = models.OneToOneField('expert.ExpertUser', on_delete=models.CASCADE, verbose_name="فرم استاد",
                                       null=True, blank=True)
    expert_firstname = models.CharField(max_length=32, verbose_name="نام")
    expert_lastname = models.CharField(max_length=32, verbose_name="نام خانوادگی")
    special_field = models.CharField(max_length=256, verbose_name="حوزه تخصصی")
    national_code = models.CharField(max_length=15, verbose_name="کد ملی")
    scientific_rank_choice = (
        (1, 'مربی'),
        (2, 'استادیار'),
        (3, 'دانشیار'),
        (4, 'استاد'),
        (5, 'استاد تمام'),
        (6, 'پژوهشگر'),

    )
    scientific_rank = models.IntegerField(choices=scientific_rank_choice, verbose_name="مرتبه علمی")
    university = models.CharField(max_length=128, verbose_name="دانشگاه محل فعالیت")
    home_address = models.CharField(max_length=512, verbose_name="ادرس منزل")
    phone_number = models.CharField(max_length=15, verbose_name="شماره منزل")
    mobile_phone = models.CharField(max_length=15, verbose_name="شماره تلفن همراه")
    email_address = models.EmailField(max_length=254, verbose_name="ایمیل")
    eq_test = models.OneToOneField(EqTest, on_delete=models.SET_NULL, verbose_name="تست EQ", blank=True, null=True)
    awards = models.TextField(blank=True, verbose_name="افتخارات", null=True)
    method_of_introduction = models.TextField(verbose_name="طریقه اشنایی با چمران تیم", blank=True, null=True)
    positive_feature = models.TextField(verbose_name="ویژگی های مثبت چمران تیم", blank=True, null=True)
    lab_equipment = models.TextField(verbose_name="امکانات پژوهشی", blank=True, null=True)
    number_of_researcher_choice = (
        (1, '1-10'),
        (2, '11-30'),
        (3, '31-60'),
        (4, '+60'),
    )
    number_of_researcher = models.IntegerField(choices=number_of_researcher_choice,
                                               verbose_name="دانشجو تحت نظارت",
                                               blank=True, null=True)
    has_industrial_research_choice = (
        ('آری', 'آری'),
        ('خیر', 'خیر'),
    )
    has_industrial_research = models.CharField(max_length=10, choices=has_industrial_research_choice,
                                               verbose_name="همکاری با شرکت خارج دانشگاه", blank=True)
    number_of_grants = models.CharField(max_length=10, verbose_name="تعداد گرنت", blank=True, null=True)
    # technique = models.ManyToManyField('researcher.Technique', verbose_name="تکنیک" , blank=True, null=True)
    languages = models.TextField(verbose_name="تسلط بر زبان های خارجی", blank=True, null=True)
    photo = models.ImageField(upload_to=get_image_path, max_length=255, blank=True, null=True)
    keywords = models.ForeignKey(Keyword, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{first_name} {last_name}'.format(first_name=self.expert_firstname, last_name=self.expert_lastname)


class ScientificRecord(models.Model):
    degree = models.CharField(max_length=32, verbose_name="مقطع تحصیلی")
    major = models.CharField(max_length=64, verbose_name="رشته تحصیلی")
    university = models.CharField(max_length=128, verbose_name="دانشگاه")
    city = models.CharField(max_length=32, verbose_name="شهر")
    date_of_graduation = models.CharField(max_length=10, verbose_name="سال اخذ مدرک")
    expert_form = models.ForeignKey(ExpertForm, on_delete=models.CASCADE, verbose_name="فرم استاد")

    def __str__(self):
        return '{} - {}'.format(self.expert_form.expert_user, self.pk)


class ExecutiveRecord(models.Model):
    executive_post = models.CharField(max_length=64, verbose_name="سمت")
    date_start_post = models.CharField(max_length=15, verbose_name="تلریخ شروع")
    date_end_post = models.CharField(max_length=15, verbose_name="تاریخ پایان")
    city = models.CharField(max_length=32, verbose_name="شهر")
    organization = models.CharField(max_length=32, verbose_name="مجل خدمت")
    expert_form = models.ForeignKey(ExpertForm, on_delete=models.CASCADE, verbose_name="فرم استاد")


class ResearchRecord(models.Model):
    STATUS_CHOICE = (
        (1, 'در دست اجرا'),
        (2, 'خاتمه یافته'),
        (3, 'متوقف')
    )
    research_title = models.CharField(max_length=128, verbose_name="عنوان طرح")
    researcher = models.CharField(max_length=64, verbose_name="نام مجری")
    co_researcher = models.CharField(max_length=512, verbose_name="همکار")
    status = models.IntegerField(choices=STATUS_CHOICE, verbose_name="وضعیت")
    expert_form = models.ForeignKey(ExpertForm, on_delete=models.CASCADE, verbose_name="فرم استاد")


class PaperRecord(models.Model):
    research_title = models.CharField(max_length=128, verbose_name="عنوان مقاله")
    date_published = models.CharField(max_length=15, verbose_name="تاریخ انتشار")
    published_at = models.CharField(max_length=32, verbose_name="محل انتشار")
    impact_factor = models.FloatField(verbose_name="impact factor")
    citation = models.CharField(max_length=5, verbose_name="تعداد ارجاع")
    expert_form = models.ForeignKey(ExpertForm, on_delete=models.CASCADE, verbose_name="فرم استاد")


class ExpertProjectHistory(models.Model):
    project_title_english = models.CharField(max_length=128, verbose_name="عنوان مقاله")
    key_words = models.ManyToManyField('industry.Keyword', verbose_name="کلمات کلیدی")
    project_priority_level = models.FloatField(verbose_name="اولویت پروژه")
    project_start_date = models.CharField(max_length=15, verbose_name="تاریخ شروع")
    project_end_date = models.CharField(max_length=15, verbose_name="تاریخ پایان")
    STATUS_CHOICE = (
        ('completed', 'completed'),
        ('stopped', 'stopped'),
    )
    project_status = models.CharField(max_length=9, choices=STATUS_CHOICE, verbose_name="وضعیت")
    project_point = models.FloatField(verbose_name='امتیاز')
    project_income = models.IntegerField(verbose_name='درآمد')
    project_involveTech = models.CharField(max_length=500, verbose_name='تکنیک ها')
    expert = models.ForeignKey(ExpertUser, on_delete=models.CASCADE, verbose_name="استاد")

    def __str__(self):
        return "history of " + self.project_title_english


class IndustryEvaluateExpert(models.Model):
    expert = models.ForeignKey(ExpertUser, on_delete=models.CASCADE, verbose_name="استاد")
    industry = models.OneToOneField('industry.IndustryUser', on_delete=models.CASCADE,
                                    verbose_name="صنعت ارزیابی کننده", blank=True, null=True)
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

    ontime_progress_report = models.IntegerField(choices=INT_CHOICE, verbose_name="گزارش به موقع")
    contribution_to_industry = models.IntegerField(choices=INT_CHOICE, verbose_name="میزان همکاری با صنعت")
    correct_estimation = models.IntegerField(choices=INT_CHOICE, verbose_name="تخمین استاد از هزینه و مواد")
    ontime_deadline = models.IntegerField(choices=INT_CHOICE, verbose_name="زمتن بندی اجرا")
    fulfill_requirement = models.IntegerField(choices=INT_CHOICE, verbose_name="اجرا مفاد قرارداد")
    disciplined = models.IntegerField(choices=INT_CHOICE, verbose_name="تعهد کاری")
    committed_to_goals = models.IntegerField(choices=INT_CHOICE, verbose_name="تحقق اهداف پروژه")
    quality = models.IntegerField(choices=INT_CHOICE, verbose_name="کیفیت عملکرد")
    total_satisfaction = models.IntegerField(choices=INT_CHOICE, verbose_name="رضایت کلی")
    continue_cooperate = models.BooleanField(choices=BOOL_CHOICE, verbose_name="ادامه همکاری با استاد")
    continue_with_chamt = models.BooleanField(choices=BOOL_CHOICE, verbose_name="ادامه همکاری با چمران تیم")
    has_innovation = models.BooleanField(choices=BOOL_CHOICE, verbose_name="دارای طرح جدید")

    def average(self):
        sum = 0.0
        sum = self.ontime_progress_report + self.contribution_to_industry + self.correct_estimation + self.ontime_deadline
        sum = sum + self.fulfill_requirement + self.committed_to_goals + self.total_satisfaction + self.quality + self.disciplined

        ava = float(sum / 8)
        return ava


class ResearcherEvaluateExpert(models.Model):
    expert = models.ForeignKey(ExpertUser, on_delete=models.CASCADE, verbose_name="")
    researcher = models.OneToOneField('researcher.ResearcherUser', on_delete=models.CASCADE, verbose_name="",
                                      blank=True, null=True)
    INT_CHOICE = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    tech_enough_info = models.IntegerField(choices=INT_CHOICE, verbose_name="اطاعات لازم نحوه کار تکنیک ها")
    tech_required_info = models.IntegerField(choices=INT_CHOICE, verbose_name="صحت تکنیک های مورد نیاز")
    total_gain = models.IntegerField(choices=INT_CHOICE, verbose_name="افزایش یادگیری")
    scientific_level = models.IntegerField(choices=INT_CHOICE, verbose_name="سطح علمی استاد")
    availability = models.IntegerField(choices=INT_CHOICE, verbose_name="در دسترس بودن")
    planing = models.IntegerField(choices=INT_CHOICE, verbose_name="تناسب برنامه با زمان دانشجو")
    flexible_schedule = models.IntegerField(choices=INT_CHOICE, verbose_name="انعطاف برنامه استاد")
    formal_act = models.IntegerField(choices=INT_CHOICE, verbose_name="برخورد محترمانه")
    distribute_task = models.IntegerField(choices=INT_CHOICE, verbose_name="به کارگیری متعادل دانشجویان")
    total_satisfaction = models.IntegerField(choices=INT_CHOICE, verbose_name="رضایت کلی")
    chamt_satisfaction = models.IntegerField(choices=INT_CHOICE, verbose_name="رضایت از چمران تیم")
    next_cooperation = models.IntegerField(choices=INT_CHOICE, verbose_name="")
    fulfill_requirements = models.IntegerField(choices=INT_CHOICE, verbose_name="تامین مالی و ازمایشگاه")

    def average(self):
        sum = 0.0
        sum += self.tech_enough_info + self.tech_required_info + self.total_gain + self.scientific_level
        sum += self.availability + self.planing + self.formal_act + self.distribute_task
        sum += self.total_satisfaction + self.chamt_satisfaction + self.next_cooperation + self.fulfill_requirements

        ava = float(sum / 12)
        return ava


class ResearchGain(models.Model):
    GAIN_CHOICE = (
        (1, 'تجریه عملی'),
        (2, 'استاد به عنوان معرف عمل کرده'),
        (3, 'مشارکت در مقاله'),
        (4, 'دریافت پیشنهاد کار'),
        (5, 'از قبل انجام کار پول دریافت کردم'),
    )
    researcher_evaluate_expert = models.ForeignKey(ResearcherEvaluateExpert, on_delete=models.CASCADE,
                                                   verbose_name="استاد")
    research_gain = models.IntegerField(choices=GAIN_CHOICE, verbose_name="دستاورد دانشجو")

class ResearchQuestion(models.Model):
    question_title = models.CharField(max_length=128, verbose_name="عنوان سوال")
    submitted_date = models.DateField(auto_now_add=True, verbose_name="تاریخ ثبت سوال")
    question_text = models.TextField(verbose_name="سوال")
    attachment = models.FileField(upload_to=get_attachment_path, verbose_name="ضمیمه", null=True, blank=True)
    uniqe_id = models.UUIDField(unique=True , default=uuid.uuid4)

    STATUS = [
        ('waiting', 'در حال بررسی'),
        ('not_answered', 'در انتظار پاسخ'),
        ('answered', 'پاسخ داده شده'),
    ]
    status = models.CharField(max_length=16, choices=STATUS, verbose_name="وضعیت", default="waiting")

    expert = models.ForeignKey(ExpertUser, on_delete=models.DO_NOTHING, verbose_name="استاد")

    def __str__(self):
        return self.question_title

    def get_answer_number(self):
        answers_number = models.ResearchQuestionInstance.objects.filter(research_question=self).count()
        return int(answers_number)

    def get_answers(self):
        answers = models.ResearchQuestionInstance.objects.filter(research_question=self)
        return answers