from django.shortcuts import render
from django.http import JsonResponse

from industry.models import IndustryUser, Project
from expert.models import ExpertUser
from researcher.models import ResearcherUser

def projectName(request, project_id):
    try:
        project = Project.objects.get(project)
        data = {
            'project_name': project.project_form.name,
            'creator': project.creator,
        }
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