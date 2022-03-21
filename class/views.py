from django.http import HttpResponse
from django.shortcuts import render
from dashboard.models import Classroom
from datetime import datetime
from .models import Assignment, Topic
from django.template.defaultfilters import slugify

# Create your views here.
def index(request, class_id):
    return render(request, "class/index.html", {
        "classroom": Classroom.objects.get(join_code=class_id)
    })

def post_assignment(request, class_id):
    classroom = Classroom.objects.get(join_code=class_id)
    if request.method == "POST":
        print(request.POST["due"])
        date_time_obj = datetime.strptime(request.POST.get("due"), '%Y-%m-%dT%H:%M')
        assignment = Assignment.objects.create(title=request.POST.get("title"), description=request.POST.get("description"), classroom=classroom, points=request.POST.get("points"), due=date_time_obj, slug=slugify(request.POST["title"]))

        return HttpResponse(assignment.slug)
    else:
        return render(request, "class/post-assignment.html", {
            "classroom": classroom
        })
