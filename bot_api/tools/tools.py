import expert.models as expert_models
import industry.models as industry_models
import researcher.models as researcher_models



from persiantools.jdatetime import JalaliDate


def gregorian_to_numeric_jalali(date):
    if date is None:
        return "نامشخص"
    j_date = JalaliDate(date)
    return str(j_date.year) + '/' + str(j_date.month) + '/' + str(j_date.day)

def JalaliToGregorianDate(date):
    datePart = date.split("/")
    return JalaliDate(year=int(datePart[0]), month=int(datePart[1]), day=int(datePart[2]))\
        .to_gregorian()

def jalali_date(jdate):
    jalali_months = ('فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر',
                     'دی', 'بهمن', 'اسفند')
    return str(jdate.day) + ' ' + jalali_months[jdate.month - 1] + ' ' + str(jdate.year)

def find_account_type(user):
    expert = expert_models.ExpertUser.objects.filter(user=user)
    if expert.exists():
        return 'expert'
    industry = industry_models.IndustryUser.objects.filter(user=user)
    if industry.exists():
        return 'industry'
    researcher = researcher_models.ResearcherUser.objects.filter(user=user)
    if researcher.exists():
        return 'researcher'
    else:
        return False


def find_user(user, account_type=None):
    if account_type is None:
        account_type = find_account_type(user)
    if account_type == 'expert':
        return user.expertuser
    elif account_type == 'researcher':
        return user.researcheruser
    elif account_type == 'industry':
        return user.industryuser
    else:
        return False


def get_user_by_unique_id(unique):
    expert = expert_models.ExpertUser.objects.filter(unique__exact=unique)
    if expert.exists():
        return expert.first(), "expert"
    
    industry = industry_models.IndustryUser.objects.filter(unique__exact=unique)
    if industry.exists():
        return industry.first(), "industry"
    
    researcher = researcher_models.ResearcherUser.objects.filter(unique__exact=unique)
    if researcher.exists():
        return researcher.first(), "researcher"
    return None

def get_user_fullname(user, account_type=None):
    if account_type == None:
        account_type = find_account_type(user)
    if account_type == 'researcher':
        return user.researcheruser.researcherprofile.fullname
    elif account_type == 'expert':
        return user.expertuser.expertform.fullname
    elif account_type == "industry":
        return user.industryuser.profile.name

def get_persian_account_type(account_type):
    if account_type == "expert":
        return "استاد"
    elif account_type == "researcher":
        return "پژوهشگر"
    elif account_type == "industry":
        return "صنعت"
    else:
        return None 