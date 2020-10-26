import datetime
import json
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import HttpResponse

from persiantools.jdatetime import JalaliDate ,digits

from chamran_admin.views import Handler403
from chamran_admin.models import Task, Card
from .views import sendMessage

RED_EXCLAMTION_MARK = "\U00002757"
RED_TRIANGLE_POINTED_DOWN = "\U0001F53B"
PENCIL_SELECTOR = "\U0000270F\U0000FE0F"
LABEL = '\U0001F3F7'
HOURGLASS_NOT_DONE = "\U000023F3"

def gregorian_to_numeric_jalali(date):
    if date:
        j_date = JalaliDate(date)
        return digits.en_to_fa(str(j_date.year)) + '/' + digits.en_to_fa(str(j_date.month)) + '/' + digits.en_to_fa(str(j_date.day))
    else:
        return "نا مشخص"


def taskReminder():

    TEXT = """{red_exclamtion_1} فقط {remaind_time} تا پایان مهلت {field} زیر باقی مانده {red_exclamtion_2}

{label} نام: {name}
{pencil}افراد مسئول: {involved_users}
{hourglass}مهلت انجام: {deadline}

{red_triangle} برای اطلاعات بیشتر می توانید دکمه «مشاهده پروژه» در زیر این پیام را بزنید."""

    allTasks = Task.objects.filter(done=False).exclude(deadline=None)
    for task in allTasks:
        weeklyPeriod = task.deadline - datetime.timedelta(days=+7)
        dailyPeriod = task.deadline - datetime.timedelta(days=+1)
        today = datetime.datetime.now(datetime.timezone.utc).date()

        if today < weeklyPeriod:
            break

        if today == weeklyPeriod:
            url = "https://chamranteam.ir/project/"+str(task.project.code)
            text = TEXT.format(red_exclamtion_1=RED_EXCLAMTION_MARK,
                               remaind_time="یک هفته",
                               field="وظیفه (تسک)",
                               label=LABEL,
                               red_exclamtion_2=RED_EXCLAMTION_MARK,
                               name=task.description,
                               pencil=PENCIL_SELECTOR,
                               involved_users=" ,".join(task.get_involved_users()),
                               hourglass=HOURGLASS_NOT_DONE,
                               deadline=gregorian_to_numeric_jalali(task.deadline),
                               red_triangle=RED_TRIANGLE_POINTED_DOWN)
            sendMessage(project=task.project, text=text, url=url)

        elif today == dailyPeriod:
            url = "https://chamranteam.ir/project/"+str(task.project.code)
            text = TEXT.format(red_exclamtion_1=RED_EXCLAMTION_MARK,
                               remaind_time="یک روز",
                               field="وظیفه (تسک)",
                               label=LABEL,
                               red_exclamtion_2=RED_EXCLAMTION_MARK,
                               name=task.description,
                               pencil=PENCIL_SELECTOR,
                               involved_users=" ,".join(task.get_involved_users()),
                               hourglass=HOURGLASS_NOT_DONE,
                               deadline=gregorian_to_numeric_jalali(task.deadline),
                               red_triangle=RED_TRIANGLE_POINTED_DOWN)
            sendMessage(project=task.project, text=text, url=url)
    
    return



def cardReminder():

    TEXT = """{red_exclamtion_1} فقط {remaind_time} تا پایان مهلت {field} زیر باقی مانده {red_exclamtion_2}

{label} نام: {name}
{hourglass}مهلت انجام: {deadline}

{red_triangle} برای اطلاعات بیشتر می توانید دکمه «مشاهده پروژه» در زیر این پیام را بزنید."""


    allCards = Card.objects.all()
    for card in allCards:
        weeklyPeriod = card.deadline - datetime.timedelta(days=+7)
        dailyPeriod = card.deadline - datetime.timedelta(days=+1)
        today = datetime.datetime.now(datetime.timezone.utc).date()
        if today < weeklyPeriod:
            break

        if today == weeklyPeriod:
            text = TEXT.format(red_exclamtion_1=RED_EXCLAMTION_MARK,
                                red_exclamtion_2=RED_EXCLAMTION_MARK,
                                remaind_time="یک هفته",
                                field="سررسید (ددلاین)",
                                label=LABEL,
                                name=card.title,
                                hourglass=HOURGLASS_NOT_DONE,
                                deadline=gregorian_to_numeric_jalali(card.deadline),
                                red_triangle=RED_TRIANGLE_POINTED_DOWN)
            url = "https://chamranteam.ir/project/"+str(card.project.code)
            sendMessage(project=card.project, text=text, url=url)

        elif today == dailyPeriod:
            text = TEXT.format(red_exclamtion_1=RED_EXCLAMTION_MARK,
                                red_exclamtion_2=RED_EXCLAMTION_MARK,
                                remaind_time="یک روز",
                                field="سررسید (ددلاین)",
                                label=LABEL,
                                name=card.title,
                                hourglass=HOURGLASS_NOT_DONE,
                                deadline=gregorian_to_numeric_jalali(card.deadline),
                                red_triangle=RED_TRIANGLE_POINTED_DOWN)
            url = "https://chamranteam.ir/project/"+str(card.project.code)
            sendMessage(project=card.project, text=text, url=url)
    
    return


def reminder(request):
    try:
        inputData = json.loads(request.body)
        if inputData['secretCode'] == "k#L^xvG!z2PjN7CN_?*5GbkKCL49K*ym!cc_hR+R?Kzg$hA?9ZrGA2RYJgK&Nh5q":
            taskReminder()
            cardReminder()
        else:
            return Handler403(request)
    except:
        send_mail(subject="Chamran Team Reminder Error",
                  message="There is a problem with task and card reminder. Please check the server.",
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=["a.jafarzadeh1998@gmail.com", ])#'sepehr.metanat@gmail.com'])
        return Handler403(request, Exception())
    return HttpResponse("OK")