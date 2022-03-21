from django.shortcuts import redirect, render
from .models import Classroom, StudentClassroom, TeacherClassroom
from helpers import random_str
from itertools import chain

# Create your views here.
def view_all_classrooms(request):
    s = StudentClassroom.objects.filter(user=request.user)
    t = TeacherClassroom.objects.filter(user=request.user)
    classrooms = list(chain(s, t))

    return render(request, "dashboard/index.html" , {
        "classrooms": classrooms
    })

def create_classroom(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        join_code = random_str()

        c = Classroom.objects.create(title=title, description=description, owner=request.user, join_code=join_code)
        TeacherClassroom.objects.create(user=request.user, classroom=c)

        return redirect("/")

    else:
        return render(request, "dashboard/create.html")

