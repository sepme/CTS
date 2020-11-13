import bot_api.views as views
import expert.models as expert_models
import researcher.models as researcher_models
import telegram


def sendMessage(group_set, text, url=None):
    if url is None:
        for gp in group_set:
            bot.sendMessage(chat_id=gp.group_id, text=text)
    else:
        keyboard = [[telegram.InlineKeyboardButton("مشاهده پروژه", url=url)],]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        for gp in group_set:
            bot.sendMessage(chat_id=gp.group_id, text=text.replace("<br>", "\n"), reply_markup=reply_markup)


def suggestProjectToExpert(title, industry_name, project_code):
    url = "https://chamranteam.ir/project/" + project_code
    keyboard = [[telegram.InlineKeyboardButton("مشاهده پروژه", url=url)],]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    for expert in expert_models.ExpertUser.objects.exclude(status='inactivated'):
        if expert.chat_id is not None:
            text = """پروژه : {project_title}\n توسط : {industry_name}\n برروی سایت قرار گرفته است. برای مشاهده جزیات بیشتر پروژه دکمه مشاهده در پایین پیام را فشار دهید.""".\
                format(project_title=title,
                    industry_name=industry_name,)
            views.bot.sendMessage(chat_id=expert.chat_id, text=text, reply_markup=reply_markup)
    
    return

def suggestProjectToResearcher(title, industry_name, project_code, techniques_list):
    projectTech = set([str(tech) for tech in techniques_list])
    url = "https://chamranteam.ir/project/" + project_code
    keyboard = [[telegram.InlineKeyboardButton("مشاهده پروژه", url=url)],]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    for researcher in researcher_models.ResearcherUser.objects.filter(status__status="free"):
        suggest = True
        researcherTechs = set([str(tech.technique) for tech in researcher.techniqueinstance_set.all()])
        for tech in projectTech:
            if tech not in researcherTechs:
                suggest = False
                break
        if suggest and researcher.chat_id is not None:
            TEXT = """پروژه : {project_title}\n توسط : {industry_name}\n%%\n برروی سایت قرار گرفته است. برای مشاهده جزیات بیشتر پروژه دکمه مشاهده در پایین پیام را فشار دهید.""".\
                    format(project_title=title,
                           industry_name=industry_name)
            if projectTech:
                text = TEXT.replace("%%","با مهارت های : {}".format(" ,".join(projectTech)))
            else:
                text = TEXT.replace("%%","بدون نیاز به مهارت خاص")
            views.bot.sendMessage(chat_id=researcher.chat_id, text=text, reply_markup=reply_markup)
    return
