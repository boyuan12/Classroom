from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from dashboard.models import Classroom, StudentClassroom, TeacherClassroom
from datetime import datetime
from .models import Assignment, Topic, Submission
from django.template.defaultfilters import slugify
import json
from django.views.decorators.csrf import csrf_exempt


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

def view_assignments(request, class_id):
    classroom = Classroom.objects.get(join_code=class_id)
    assignments = Assignment.objects.filter(classroom=classroom)

    return render(request, "class/assignments.html", {
        "assignments": assignments,
        "classroom": Classroom.objects.get(join_code=class_id)
    })

def view_assignment(request, class_id, assignment_slug):
    classroom = Classroom.objects.get(join_code=class_id)
    assignment = Assignment.objects.get(classroom=classroom, slug=assignment_slug)
    role = ""

    try:
        tc = TeacherClassroom.objects.get(classroom=classroom, user=request.user)
        role = "teacher"
    except TeacherClassroom.DoesNotExist:
        sc = StudentClassroom.objects.get(classroom=classroom, user=request.user)
        role = "student"

    if request.method == "POST":
        Submission.objects.create(user=request.user, assignment=assignment, text=request.POST["work"])
        return redirect(f"/classroom/{class_id}/assignment/{assignment_slug}")
    else:
        submission = None

        try:
            submission = Submission.objects.get(user=request.user, assignment=assignment)
        except Submission.DoesNotExist:
            pass

        return render(request, "class/view-assignment-student.html", {
            "assignment": assignment,
            "classroom": Classroom.objects.get(join_code=class_id),
            "role": role,
            "submission": submission
        })

@csrf_exempt
def delete_submission_api(request, class_id, assignment_slug):
    if request.method == "POST":
        # data = json.loads(request.POST)
        # class_id = data["classId"]
        # assignment_slug = data["slug"]

        classroom = Classroom.objects.get(join_code=class_id)
        assignment = Assignment.objects.get(classroom=classroom, slug=assignment_slug)

        assignment.delete()

        assignment.save()

        return JsonResponse({"success": True})