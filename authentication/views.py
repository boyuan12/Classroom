from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["password"]

        u = User.objects.create_user(first_name=first_name, last_name=last_name, username=email, email=email, password=password)

        login(request, u)

        return redirect("/")

    else:
        return render(request, "authentication/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.add_message(request, messages.ERROR, 'Incorrect login credential(s)')
            return redirect("/auth/login/")
    return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    return redirect("/auth/login/")

