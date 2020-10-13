from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from industry.models import IndustryUser, Project
from expert.models import ExpertUser
from researcher.models import ResearcherUser
import requests
import uuid

SECURITY_CODE = "BQ_?on|A5DUb_WdU4Y#4N$fL6L76$0XGpV+i%7A5jp5T3V!MkKDpXea^PRF-VLkr"

def projectName(request, project_id):
    try:
        project = Project.objects.get(code=project_id)        
        data = {
            'project_name': project.project_form.persian_title,
            'creator': project.industry_creator.profile.name,
            'creator_photo': "None",
        }
        if project.industry_creator.profile.photo:
            data['creator_photo'] = project.industry_creator.profile.photo.url        
        return JsonResponse(data=data)
    except:
        return JsonResponse(data={"error": "the project_id is invalid"}, status=400)

def searchUsername(request, keyword):
    try:
        expert = ExpertUser.objects.get(userId=keyword)
        data = {
            "fullname" : expert.expertform.fullname,
            "photo" : "none",
        }
        if expert.expertform.photo:
            data['photo'] = expert.expertform.photo.url
        return JsonResponse(data=data)
    except:
        try:
            industry = IndustryUser.objects.get(userId=keyword)
            data = {
                "fullname" : industry.profile.name,
                "photo" : "none",
            }
            if industry.profile.photo:
                data['photo'] = industry.profile.photo.url
            return JsonResponse(data=data)
        except:
            try:
                researcher = ResearcherUser.objects.get(userId=keyword)
                data = {
                    "fullname" : researcher.researcherprofile.fullname,
                    "photo" : "none",
                }
                if researcher.researcherprofile.photo:
                    data['photo'] = researcher.researcherprofile.photo.url
                return JsonResponse(data=data)
            except:
                return JsonResponse(date={"error": 'the keyword in invalid.'}, status=400)

def sendProjectData(project):
    data = {'experts': [],
            'researchers': []
            }
    data['project'] = {'id': project.id,
                        "persian_title": project.project_form.persian_title,
                        "english_title": project.project_form.english_title,
                        "code": str(project.code),
                        }
    data["industry"] = {'username': project.industry_creator.user.get_username(),
                        "fullname": project.industry_creator.profile.name,
                        "photo_url": "None"
                        }
    if project.industry_creator.profile.photo:
        data['industry']["photo_url"] = project.industry_creator.profile.photo.url
    
    for expert in project.expert_accepted.all():
        data['experts'].append({'username': expert.user.get_username(),
                                "fullname": expert.expertform.fullname,
                                "photo_url": "None"
                                })
        if expert.expertform.photo:
            data['experts'][-1]["photo_url"] = expert.expertform.photo.url

    for researcher in project.researcher_accepted.all():
        data['researchers'].append({'username': researcher.user.get_username(),
                                    "fullname": researcher.researcherprofile.fullname,
                                    "photo_url": "None"
                                })
        if researcher.researcherprofile.photo:
            data['researchers'][-1]["photo_url"] = researcher.researcherprofile.photo.url
    response = requests.post(url="https://chamranteam.pythonanywhere.com/add_project/",json=data)
    return JsonResponse(data=data)
    # return HttpResponse("OK")

def updateBotUser(typeUser, projectId ,username, fullname, photo):
    data = {
        "typeUser": typeUser,
        "projectId": projectId,
        "username": username,
        "fullname": fullname,
        "photo": "none",
    }
    if photo:
        data['photo'] = photo.url

    response = requests.post(url="https://chamranteam.pythonanywhere.com/update_user/",json=data)
    if response.status_code == 200:
        if typeUser == "expert":
            sendMessage(projectId=projectId, text="""استاد {} به این پروژه اضافه شدند.""".format(fullname))
        elif typeUser == "researcher":
            sendMessage(projectId=projectId, text="""پژوهشگر {} به این پروژه اضافه شدند.""".format(fullname))
    return

def sendMessage(projectId, text):
    data = {
        "securityCode":SECURITY_CODE,
        "id": projectId,
        "text": text
    }
    response = requests.post(url="https://chamranteam.pythonanywhere.com/send_message/",json=data)
    return

def updateTask(projectId, description, involved_username, deadline=None):
    data = {
        "id": projectId,
        "description": description,
        "deadline": deadline,
        "involved_user": involved_username,
    }
    return requests.post(url="https://chamranteam.pythonanywhere.com/add_task/",json=data)

def updateCard(projectId, title, deadline):
    data = {
        "id": projectId,
        "title": title,
        "deadline": str(deadline),
    }
    return requests.post(url="https://chamranteam.pythonanywhere.com/add_card/",json=data)
    