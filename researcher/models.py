from django.db import models
from django.contrib.auth.models import User

class Researcher(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE)
    profile       = models.OneToOneField("Profile", verbose_name=("مشخصات فردی"), on_delete=models.CASCADE)
    membershipFee = models.OneToOneField("membershipFee", verbose_name=("حق عضویت"), on_delete=models.CASCADE)
    points        = models.FloatField(blank=True ,verbose_name ='امتیاز')

    def __str__(self):
        return self.profile.name


class MembershipFee(models.Model):
    fee    =  models.IntegerField(verbose_name = 'هزینه')
    start  =  models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "اولین پرداخت")
    rePay  =  models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "آخرین پرداخت")

    def __str__(self):
        return str(self.fee)

class Profile(models.Model):
    name   =  models.CharField( max_length=300 ,verbose_name = "نام و نام خانوادگی")
    major  =  models.CharField( max_length=300 ,verbose_name = "رشته تحصیلی")
    
    GARADE_CHOICE = (
        ('bs', 'کارشناسی'),
        ('ms', 'کارشناسی ارشد'),
        ('phd', 'دکتری'),
        ('proPhd', 'دکتری حرفه‌ای'),
        )
    grade       =  models.CharField( max_length=6 ,choices = GARADE_CHOICE ,verbose_name = "آخرین مدرک تحصیلی")
    university  =  models.CharField( max_length=300 ,verbose_name = "دانشگاه محل تحصیل")
    entryYear   =  models.IntegerField(verbose_name = "سال ورود")
    address     =  models.CharField( max_length=500 ,verbose_name = "آدرس محل سکونت")
    homeNumber  =  models.CharField( max_length=50 ,verbose_name = "تلفن منزل")
    phoneNumebr =  models.CharField( max_length=50 ,verbose_name = "تلفن همراه")
    email       =  models.EmailField(max_length=254 ,verbose_name = "پست الکترونیکی")

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

    teamWork        =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "روحیه کار تیمی")
    creative        =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "تفکر خلاقانه")
    interestInMajor =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "علاقه به رشته تحصیلی")
    motivation      =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "انگیزه داشتن برای انجام پروژه")
    Sacrifice       =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "تعهد داشتن و از خود گذشتگی")
    diligence       =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "پشتکار")
    interestInlearn =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "علاقه به یادگیری")
    Timeliness      =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "وقت­شناسی")
    dataCollection  =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "جمع­ آوری داده­ ها")
    AwarenessOfPrinciples  = models.IntegerField(choices= INT_CHOICE ,verbose_name = "آگاهی از اصول انجام پروژه")

    Description     =  models.TextField()

    def __str__(self):
        return self.name + " profile"

class ScientificHistory(models.Model):
    profile = models.ForeignKey("Profile", verbose_name="سوابق علمی", on_delete=models.CASCADE)

    grade           =  models.CharField( max_length=300 ,verbose_name = "مقطع تحصیلی")
    major           =  models.CharField( max_length=300 ,verbose_name = "رشته تحصیلی")
    university      =  models.CharField( max_length=300 ,verbose_name = "دانشگاه")
    place           =  models.CharField( max_length=300 ,verbose_name = "شهر محل تحصیل")
    graduatedYear   =  models.IntegerField(verbose_name = "سال اخذ مدرک")
    
    def __str__(self):
        return self.grade

class Record(models.Model):
    profile = models.ForeignKey("Profile", verbose_name="سوابق اجرایی", on_delete=models.CASCADE)

    post   =  models.CharField( max_length=300 ,verbose_name = "سمت")
    start  =  models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "از تاریخ")
    end    =  models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تا تاریخ")
    place  =  models.CharField( max_length=300 ,verbose_name = "محل خدمت")
    city   =  models.CharField( max_length=300 ,verbose_name = "شهر")

    def __str__(self):
        return self.post

class ResearchActivities(models.Model):
    profile = models.ForeignKey("Profile", verbose_name= "سوابق پژوهشی", on_delete=models.CASCADE)

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
    profile     = models.ForeignKey("Profile", verbose_name=("تاریخچه"), on_delete=models.CASCADE)

    title       = models.CharField( max_length=300,  verbose_name=("عنوان پروژه"))
    start       = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ شروع")
    end         = models.DateField(auto_now=False, auto_now_add=False ,verbose_name = "تاریخ پایان")
    STATUS_CHOICE = (
        ('completed' ,'completed'),
        ('stoped' ,'stoped'),
    )
    status      = models.CharField( max_length=9 ,choices = STATUS_CHOICE ,verbose_name="وضعیت")
    point       = models.FloatField(verbose_name='امتیاز')
    income      = models.IntegerField(verbose_name= 'درآمد')
    involveTech = models.CharField(max_length=500 ,verbose_name='تکنیک ها')

    def __str__(self):
        return "history of " + self.profile.name 
    
class Evaluation(models.Model):
    researcher = models.ForeignKey("Researcher", on_delete=models.CASCADE)
    
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

    timeAssign          =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "به چه میزان دانشجو مطابق زمان از پیش اعلام شده در هفته، برای کار زمان تخصیص داد؟ ")
    flexibility         =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت شما از انعطاف زمانبندی ارائه شده توسط دانشجو، چقدر است؟")
    masteryTechniq      =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "دانشجو تسلط بر تکنیک های اعلام شده چه میزان بوده است؟ ")
    verificationRecords =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "صحت سوابق و مهارتهای اعلام شده توسط دانشجو چقدر بوده است؟")
    professional        =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت شما از رفتار حرفه ای دانشجو، چه اندازه است؟")
    cooperation         =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "دانشجو چه میزان همکاری سازنده با سایر اعضای تیم داشته است؟(کمک به ارتقای سطح دانش علمی و عملی گروه)")
    satisfaction        =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت شما از دانشجو در ازای ارائه نتایج عملکرد به شما چقدر بوده است ؟")
    totalSatisfaction   =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت کلی شما از دانشجو چه اندازه است؟")
    nextCooperation     =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "چقدر تمایل دارید در همکاری های بعدی با دانشجو همکاری کنید؟")
    chamranTeam         =  models.IntegerField(choices= INT_CHOICE ,verbose_name = "میزان رضایت شما از عملکرد چمران تیم در این پروژه چقدر بوده است؟")

    def avarage(self):
        sum = 0.0
        sum = self.timeAssign + self.flexibility + self.masteryTechniq + self.verificationRecords
        sum = sum + self.professional + self.cooperation + self.satisfaction + self.totalSatisfaction
        sum = sum + self.nextCooperation + self.chamranTeam
        ava = float(sum / 10)
        return ava

class Technique(models.Model):
    TYPE = (
        ('molecularBiology'    , 'Molecular Biology'),
        ('immunology'          , 'Immunology'),
        ('imaging'             , 'Imaging'),
        ('histology'           , 'Histology'),
        ('generalLab'          , 'General Lab'),
        ('animalLab'           , 'Animal Lab'),
        ('labSafety'           , 'Lab Safety'),
        ('biochemistry'        , 'Biochemistry'),
        ('cellularBiology'     , 'Cellular Biology'),
        ('researchMethodology' , 'Research Methodology'),
    )

    techniqType  = models.CharField(max_length=100 ,choices = TYPE)
    techniqTitle = models.CharField(max_length=300 )

class TechniqueInstance(models.Model):
    researcher = models.ForeignKey("Researcher", verbose_name=_(""), on_delete=models.CASCADE)
    technique  = models.OneToOneField("Technique", verbose_name="مهارت", on_delete=models.CASCADE)
    level      = models.CharField( max_length=100 ,verbose_name='سطح مهارت')
    evaluator  = models.CharField( max_length=300 ,verbose_name='ارزیابی کننده')