from django.db import models
from django.contrib.auth.models import User

import datetime

class Researcher(models.Model):
    user               =  models.OneToOneField(User, on_delete=models.CASCADE)
    researcher_profile =  models.OneToOneField("Researcher_profile", verbose_name=("مشخصات فردی"), on_delete=models.CASCADE ,blank=True)
    membership_fee     =  models.OneToOneField("Membership_fee", verbose_name=("حق عضویت"), on_delete=models.CASCADE ,blank=True)
    status             =  models.OneToOneField("Status", on_delete=models.CASCADE ,blank=True)
    points             =  models.FloatField(default=0 ,verbose_name ='امتیاز' ,blank=True)
    
    def __str__(self):
        return self.researcher_profile.name

class Status(models.Model):
    STATUS =(
        ('signed_up' ,"فرم های مورد نیاز تکمیل نشده است. "),
        ('not_answered' ,"به سوال پژوهشی پاسخ نداده است."),
        ('free' ,"فعال - بدون پروژه"),
        ('waiting' ,"فعال - در حال انتظار پروژه"),
        ('involved' ,"فعال - درگیر پروژه"),
        ('inactivated' ,"غیر فعال - تویط مدیر سایت غیر فعال شده است."),
    )
    status              = models.CharField( max_length=15 ,choices=STATUS)
    inactivate_duration = models.DateTimeField( auto_now=False, auto_now_add=False ,blank=True)

    def is_inactivate(self):
        return datetime.datetime.now() < self.inactivate_duration

class Membership_fee(models.Model):
    fee    =  models.IntegerField(verbose_name = 'هزینه')
    start  =  models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "اولین پرداخت")
    rePay  =  models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "آخرین پرداخت")

    def __str__(self):
        return str(self.fee)

class Researcher_profile(models.Model):
    name       =  models.CharField( max_length=300 ,verbose_name = "نام و نام خانوادگی")
    birth_year =  models.DateField( auto_now=False, auto_now_add=False ,verbose_name = "سال تولد")
    major      =  models.CharField( max_length=300 ,verbose_name = "رشته تحصیلی")
    
    GARADE_CHOICE = (
        ('bs', 'کارشناسی'),
        ('ms', 'کارشناسی ارشد'),
        ('phd', 'دکتری'),
        ('proPhd', 'دکتری حرفه‌ای'),
        )
    grade        =  models.CharField( max_length=6 ,choices = GARADE_CHOICE ,verbose_name = "آخرین مدرک تحصیلی")
    university   =  models.CharField( max_length=300 ,verbose_name = "دانشگاه محل تحصیل")
    entry_year   =  models.IntegerField(verbose_name = "سال ورود")
    address      =  models.CharField( max_length=500 ,verbose_name = "آدرس محل سکونت" ,blank=True)
    home_number  =  models.CharField( max_length=50 ,verbose_name = "تلفن منزل")
    phone_numebr =  models.CharField( max_length=50 ,verbose_name = "تلفن همراه",blank=True)
    email        =  models.EmailField(max_length=254 ,verbose_name = "پست الکترونیکی")

    one   = 1
    two   = 2
    three = 3
    four  = 4
    five  = 5
    INT_CHOICE =(
            (one   , '1'),
            (two   , '2'),
            (three , '3'),
            (four  , '4'),
            (five  , '5'),
    )

    team_work                =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "روحیه کار تیمی")
    creative                 =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "تفکر خلاقانه")
    interest_in_major        =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "علاقه به رشته تحصیلی")
    motivation               =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "انگیزه داشتن برای انجام پروژه")
    sacrifice                =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "تعهد داشتن و از خود گذشتگی")
    diligence                =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "پشتکار")
    interest_in_learn        =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "علاقه به یادگیری")
    timeliness               =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "وقت­شناسی")
    data_collection          =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "جمع­ آوری داده­ ها")
    awareness_of_principles  =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "آگاهی از اصول انجام پروژه")

    Description              =  models.TextField()

    def __str__(self):
        return self.name + " profile"

class ScientificHistory(models.Model):
    researcher_profile = models.ForeignKey("Researcher_profile", verbose_name="سوابق علمی", on_delete=models.CASCADE)

    grade            =  models.CharField( max_length=300 ,verbose_name = "مقطع تحصیلی")
    major            =  models.CharField( max_length=300 ,verbose_name = "رشته تحصیلی")
    university       =  models.CharField( max_length=300 ,verbose_name = "دانشگاه")
    place            =  models.CharField( max_length=300 ,verbose_name = "شهر محل تحصیل")
    graduated_year   =  models.IntegerField(verbose_name = "سال اخذ مدرک")
    
    def __str__(self):
        return self.grade

class Record(models.Model):
    researcher_profile = models.ForeignKey("Researcher_profile", verbose_name="سوابق اجرایی", on_delete=models.CASCADE)

    post   =  models.CharField( max_length=300 ,verbose_name = "سمت")
    start  =  models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "از تاریخ")
    end    =  models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تا تاریخ")
    place  =  models.CharField( max_length=300 ,verbose_name = "محل خدمت")
    city   =  models.CharField( max_length=300 ,verbose_name = "شهر")

    def __str__(self):
        return self.post

class ResearchActivities(models.Model):
    researcher_profile = models.ForeignKey("Researcher_profile", verbose_name= "سوابق پژوهشی", on_delete=models.CASCADE)

    title         =  models.CharField( max_length=300 ,verbose_name ="عنوان طرح پژوهشی")
    presenter     =  models.CharField( max_length=50 ,verbose_name ="نام مجری")
    Responsible   =  models.CharField( max_length=50 ,verbose_name ="مسئول اجرا / همکار")
    STATUS_CHOICE = (
        ('running' ,'در دست اجرا'),
        ('finished' ,'خاتمه یافته'),
        ('stoped' ,'متوقف'),
    )
    status        = models.CharField( max_length=8 ,choices= STATUS_CHOICE ,verbose_name ="وضعیت طرح پژوهشی")

    def __str__(self):
        return self.title

class History(models.Model):
    researcher_profile     = models.ForeignKey("Researcher_profile", verbose_name="تاریخچه", on_delete=models.CASCADE)

    title       = models.CharField( max_length=300,  verbose_name=("عنوان پروژه"))
    start       = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ شروع")
    end         = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ پایان")
    STATUS_CHOICE = (
        ('completed' ,'completed'),
        ('stoped' ,'stoped'),
    )
    status       = models.CharField( max_length=9 ,choices = STATUS_CHOICE ,verbose_name="وضعیت")
    point        = models.FloatField(verbose_name='امتیاز')
    income       = models.IntegerField(verbose_name= 'درآمد')
    involve_tech = models.CharField(max_length=500 ,verbose_name='تکنیک ها')

    def __str__(self):
        return "history of " + self.researcher_profile.name 
    
class Evaluation(models.Model):
    researcher = models.ForeignKey("Researcher", on_delete=models.CASCADE)
    evaluator  = models.OneToOneField("expert.Expert", on_delete=models.CASCADE)
    
    zero  = 0
    one   = 1
    two   = 2
    three = 3
    four  = 4
    five  = 5
    INT_CHOICE =(
            (one   , '1'),
            (two   , '2'),
            (three , '3'),
            (four  , '4'),
            (five  , '5'),
    )

    time_assign          =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "به چه میزان دانشجو مطابق زمان از پیش اعلام شده در هفته، برای کار زمان تخصیص داد؟ ")
    flexibility          =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت شما از انعطاف زمانبندی ارائه شده توسط دانشجو، چقدر است؟")
    mastery_techniq      =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "دانشجو تسلط بر تکنیک های اعلام شده چه میزان بوده است؟ ")
    verification_records =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "صحت سوابق و مهارتهای اعلام شده توسط دانشجو چقدر بوده است؟")
    professional         =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت شما از رفتار حرفه ای دانشجو، چه اندازه است؟")
    cooperation          =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "دانشجو چه میزان همکاری سازنده با سایر اعضای تیم داشته است؟(کمک به ارتقای سطح دانش علمی و عملی گروه)")
    satisfaction         =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت شما از دانشجو در ازای ارائه نتایج عملکرد به شما چقدر بوده است ؟")
    total_satisfaction   =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت کلی شما از دانشجو چه اندازه است؟")
    next_cooperation     =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "چقدر تمایل دارید در همکاری های بعدی با دانشجو همکاری کنید؟")
    chamran_team         =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت شما از عملکرد چمران تیم در این پروژه چقدر بوده است؟")

    def avarage(self):
        sum = 0.0
        sum = self.time_assign + self.flexibility + self.mastery_techniq + self.verification_records
        sum = sum + self.professional + self.cooperation + self.satisfaction + self.total_satisfaction
        sum = sum + self.next_cooperation + self.chamran_team
        ava = float(sum / 10)
        return ava

class Technique(models.Model):
    TYPE = (
        ('molecular_biology'   , 'Molecular Biology'),
        ('immunology'          , 'Immunology'),
        ('imaging'             , 'Imaging'),
        ('histology'           , 'Histology'),
        ('general_lab'         , 'General Lab'),
        ('animal_lab'          , 'Animal Lab'),
        ('lab_safety'          , 'Lab Safety'),
        ('biochemistry'        , 'Biochemistry'),
        ('cellular_biology'    , 'Cellular Biology'),
        ('research_methodology', 'Research Methodology'),
    )

    techniq_type  = models.CharField( max_length=100 ,choices = TYPE)
    techniq_title = models.CharField( max_length=300 )
    tutorial_link = models.CharField( max_length=500 )

class TechniqueInstance(models.Model):
    researcher = models.ForeignKey("Researcher", on_delete=models.CASCADE)
    technique  = models.OneToOneField("Technique", verbose_name="مهارت", on_delete=models.CASCADE)
    TECH_GRADE = (
        ('A' ,'به صورت عملی در پروژه انجام داده است.'),
        ('B' ,'به صورت عملی در کارگاه آموزش دیده است.'),
        ('C' ,'به صورت تئوری آموزش دیده است.'),
    )
    level      = models.CharField( max_length=1 ,choices=TECH_GRADE ,verbose_name='سطح مهارت' ,blank=True)
    evaluator  = models.CharField( max_length=300 ,verbose_name='ارزیابی کننده',blank=True)

    def is_validated(self):
        if self.level == 'A' or self.level == 'B' or self.level == 'C':
            return True
        return False

class RequestedProject(models.Model):
    researcher          = models.ForeignKey("Researcher", on_delete=models.CASCADE)
    project             = models.OneToOneField("industry.Project", on_delete=models.CASCADE)
    date_requested      = models.DateField(auto_now=False, auto_now_add=False ,verbose_name='تاریخ درخواست')
    least_hours_offered = models.IntegerField(default=0 ,verbose_name='حداقل مدت زمانی پیشنهادی در هفته')
    most_hours_offered  = models.IntegerField(default=0 ,verbose_name='حداکثر مدت زمانی پیشنهادی در هفته')