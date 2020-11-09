from expert.models import ExpertUser
from industry.models import IndustryUser
from researcher.models import ResearcherUser



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
    expert = ExpertUser.objects.filter(user=user)
    if expert.exists():
        return 'expert'
    industry = IndustryUser.objects.filter(user=user)
    if industry.exists():
        return 'industry'
    researcher = ResearcherUser.objects.filter(user=user)
    if researcher.exists():
        return 'researcher'
    else:
        return False


def find_user(user):
    if find_account_type(user) == 'expert':
        return user.expertuser
    elif find_account_type(user) == 'researcher':
        return user.researcheruser
    elif find_account_type(user) == 'industry':
        return user.industryuser
    else:
        return False


def get_user_by_unique_id(unique):
    expert = ExpertUser.objects.filter(unique__exact=unique)
    researcher = ResearcherUser.objects.filter(unique__exact=unique)
    industry = IndustryUser.objects.filter(unique__exact=unique)
    if expert.exists():
        return expert[0]
    elif researcher.exists():
        return researcher[0]
    elif industry.exists():
        return industry[0]
    else:
        return False

def get_user_fullname(user, account_type=None):
    if account_type == None:
        account_type = find_account_type(user)
    if account_type == 'researcher':
        return user.researcheruser.researcherprofile.fullname
    elif account_type == 'expert':
        return user.expertuser.expertform.fullname
    elif account_type == "industry":
        return user.industryuser.profile.name