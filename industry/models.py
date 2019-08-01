from django.db import models
from django.contrib.auth.models import User

from django.shortcuts import reverse ,HttpResponseRedirect

class IndustryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر صنعت")
    industry_points = models.FloatField(verbose_name="امتیاز صنعت" ,default=0.0)

    def __str__(self):
        return self.user.get_username()
    
    def get_absolute_url(self):
        return HttpResponseRedirect(reverse("industry:index", kwargs={"pk": self.pk}))


class IndustryForm(models.Model):
    industry_user = models.OneToOneField('industry.IndustryUser', on_delete=models.CASCADE, verbose_name="فرم صنعت")
    name = models.CharField(max_length=64, verbose_name="نام شرکت")
    registration_number = models.IntegerField(verbose_name="شماره ثبت")
    date_of_foundation = models.IntegerField(verbose_name="تاریخ تاسیس")
    research_field = models.CharField(max_length=32, verbose_name="حوزه فعالیت")
    industry_type_choice = (
        (0, 'خصوصی'),
        (1, 'دولتی'),
    )
    industry_type = models.IntegerField(choices=industry_type_choice, verbose_name="نوع شرکت")
    industry_address = models.TextField(verbose_name="ادرس شرکت")
    phone_number = models.IntegerField(verbose_name="شماره تلفن")
    international_activities = models.TextField(verbose_name="سابقه فعالیت بین المللی")
    tax_declaration = models.FileField(upload_to='./uploads', verbose_name="اظهارنامه مالیاتی")
    turn_over = models.FloatField(verbose_name="گردش مالی")
    services_products = models.TextField(verbose_name="خدمات/محصولات")
    awards_honors = models.TextField(verbose_name="افتخارات")
    email_address = models.EmailField(max_length=254, verbose_name="ادرس")

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=32)


class ProjectForm(models.Model):
    project_title_persian = models.CharField(max_length=128, verbose_name="عنوان پروژه فارسی")
    project_title_english = models.CharField(max_length=128, verbose_name="عنوان پروژه انگلیسی")
    key_words = models.ManyToManyField(Keyword, verbose_name="کلمات کلیدی")
    percentage_wet_lab = models.FloatField(verbose_name="درصد wet_lab")
    percentage_dry_lab = models.FloatField(verbose_name="درصد dry_lab ")
    research_methodology_choice = (
        (0, 'کیفی'),
        (1, 'کمی'),
    )
    research_methodology = models.IntegerField(choices=research_methodology_choice, verbose_name="روش تحقیق")
    main_problem_and_importance = models.TextField(verbose_name="مشکلات اصلی و اهداف")
    progress_profitability = models.TextField(verbose_name="پیشرفت های حاصل")
    approach = models.TextField(verbose_name="راه کار ها")
    innovation = models.TextField(verbose_name="نو آوری ها")
    required_lab_equipment = models.TextField(verbose_name="منابع مورد نیاز")
    required_technique = models.ManyToManyField('researcher.Technique', verbose_name="تکنیک های مورد نیاز")
    project_phase = models.TextField(verbose_name="مراحل انجام پروژه")
<<<<<<< HEAD
    required_budget = models.TextField(verbose_name="بودجه مورد نیاز" ,null=True)
    # papers_and_documentation = models.TextField(verbose_name="مقالات و مستندات" ,null=True)
=======
    required_budget = models.FloatField(verbose_name="بودجه مورد نیاز")
    papers_and_documentation = models.TextField(verbose_name="مقالات و مستندات")
>>>>>>> parent of a437e57... "Projects" Section Front-End + "Researcher Apply" Section Front-End
    policy = models.TextField(verbose_name="نکات اخلاقی")

    def __str__(self):
        return self.project_title_english


class Project(models.Model):
    project_form = models.OneToOneField(ProjectForm, on_delete=models.CASCADE, verbose_name="فرم پروژه")
    date_submitted_by_industry = models.DateField(verbose_name="تاریخ ثبت پرژه توسط صنعت")
    date_selected_by_expert = models.DateField(verbose_name="تاریخ درخواست پروژه توسط استاد")
    date_start = models.DateField(verbose_name="تاریخ اخذ پروژه توسط استاد")
    date_project_started = models.DateField(verbose_name="تاریخ شروع پروژه")
    date_phase_two_deadline = models.DateField(verbose_name="ناریخ مهلت فاز دوم")
    date_phase_three_deadline = models.DateField(verbose_name="تاریخ مهلت فاز سوم")
    date_phase_one_finished = models.DateField(verbose_name="تاریخ پایان فاز اول")
    date_phase_two_finished = models.DateField(verbose_name="تاریخ پایان فاز دوم")
    date_finished = models.DateField(verbose_name="تاریخ اتمام پروژه")
    researcher_applied = models.ManyToManyField('researcher.ResearcherUser', verbose_name="پژوهشگران درخواست داده",
                                                related_name="researchers_applied")
    researcher_accepted = models.ManyToManyField('researcher.ResearcherUser', verbose_name="پژوهشگران پذبرفته شده",
                                                 related_name="researchers_accepted")
    expert_applied = models.ManyToManyField('expert.ExpertUser', verbose_name="اساتید درخواست داده",
                                            related_name="experts_applied")
    expert_accepted = models.OneToOneField('expert.ExpertUser', on_delete=models.CASCADE,
                                           verbose_name="استاد پذیرفته شده",
<<<<<<< HEAD
                                           related_name="expert_accepted" ,null=True)

    cost_of_project = models.FloatField(verbose_name="هزینه پروژه" ,null=True)
    maximum_researcher = models.IntegerField(verbose_name="حداکثر تعداد پژوهشگر"  ,null =True)
    project_detail = models.TextField(verbose_name="جزيات پروژه" ,null =True)
    project_priority_level = models.FloatField(verbose_name="سطح اهمیت پروژه" ,null =True)
=======
                                           related_name="expert_accepted")
    industry_creator = models.OneToOneField('industry.IndustryUser', on_delete=models.CASCADE,
                                            verbose_name="صنعت صاحب پروژه")
    cost_of_project = models.FloatField(verbose_name="هزینه پروژه")
    maximum_researcher = models.IntegerField(verbose_name="حداکثر تعداد پژوهشگر")
    project_detail = models.TextField(verbose_name="جزيات پروژه")
    project_priority_level = models.FloatField(verbose_name="سطح اهمیت پروژه")
>>>>>>> parent of a437e57... "Projects" Section Front-End + "Researcher Apply" Section Front-End

    def __str__(self):
        return self.project_form

    def get_comments(self):
        project_comments = Comment.objects.all().filter(project=self)
        return project_comments


class Comment(models.Model):
    description = models.TextField(verbose_name="متن")
    SENDER = (
        (0, 'متخصص'),
        (1, 'صنعت')
    )
    sender_type = models.IntegerField(choices=SENDER)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='./project_{0}'.format(project))
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
    expert = models.OneToOneField('expert.ExpertUser', on_delete=models.CASCADE)
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
