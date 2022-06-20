from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from dashboard.models import Classroom, StudentClassroom, TeacherClassroom
from datetime import datetime
from .models import Assignment, Topic, Submission
from django.template.defaultfilters import slugify
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


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
    
        if role == "student":
            return render(request, "class/view-assignment-student.html", {
                "assignment": assignment,
                "classroom": Classroom.objects.get(join_code=class_id),
                "role": role,
                "submission": submission
            })
        else:
            submissions = Submission.objects.filter(assignment=assignment)
            submitted_student = [sub.user for sub in submissions]
            all_students = [sc.user for sc in StudentClassroom.objects.filter(classroom=classroom)]
            did_not_submit = []

            for stu in all_students:
                if stu not in submitted_student:
                    did_not_submit.append(stu)

            return render(request, "class/view-assignment-teacher.html", {
                "assignment": assignment,
                "classroom": Classroom.objects.get(join_code=class_id),
                "submissions": submissions,
                "did_not_submit": did_not_submit
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

@csrf_exempt
def score_assignment_api(request, class_id, assignment_slug):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        # class_id = data["classId"]
        # assignment_slug = data["slug"]

        submission_id = data["subId"]
        points = int(data["score"])
        
        sub = Submission.objects.get(id=int(submission_id))
        sub.points = points
        sub.save()
        
        return JsonResponse({"success": True})

def view_student_work(request, class_id, assignment_slug, stu_id):
    classroom = Classroom.objects.get(join_code=class_id)
    assignment = Assignment.objects.get(classroom=classroom, slug=assignment_slug)
    user = User.objects.get(id=stu_id)

    submission = Submission.objects.get(user=user, assignment=assignment)

    return render(request, "class/view-student-work.html", {
        "classroom": classroom,
        "assignment": assignment,
        "student": user,
        "submission": submission,
    })

def view_student_gradebook(request, class_id):
    classroom = Classroom.objects.get(join_code=class_id)
    assignments = Assignment.objects.filter(classroom=classroom)
    submissions = []


    for a in assignments:
        submission = Submission.objects.get(assignment=a, user=request.user)
        submissions.append(submission)
    

    return render(request, "class/student-gradebook.html", {
        "submissions": submissions,
        "classroom": classroom,
        "grade": calc_grade(submissions)
    })

def calc_grade(submissions):
    """
    Add all the total points and Add all the actual points and divide the actual points by the total points
    """
    possible_score = 0
    student_score = 0

    for sub in submissions:
        possible_score += sub.assignment.points
        student_score += sub.points
    
    return round(student_score / possible_score * 100, 2) 
