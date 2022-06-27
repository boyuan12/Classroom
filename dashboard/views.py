from django.shortcuts import redirect, render
from .models import Classroom, StudentClassroom, TeacherClassroom
from helpers import random_str
from itertools import chain
from django.http import HttpResponse

# Create your views here.
def view_all_classrooms(request):
    print(request.user.username)
    if request.user.username == "":
        return HttpResponse("Hello")

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

def join_classroom(request):
    if request.method == "POST":
        code = request.POST["code"]
        classroom = Classroom.objects.get(join_code=code)
        StudentClassroom.objects.create(user=request.user, classroom=classroom)

        return redirect(f"/classroom/{code}/")

    else:
        return render(request, "dashboard/join-classroom.html")
