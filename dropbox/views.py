from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import json

import cloudinary
import cloudinary.uploader
import cloudinary.api

from helpers import convert_file

cloudinary.config(
    cloud_name = "boyuan12",
    api_key = "893778436618783",
    api_secret = "X4LufXPHxvv4hROS3VZWYyR3tIE"
)

# Create your views here.
DROPBOX_APP_KEY = "2v7zl2nwu8216c3"
DROPBOX_APP_SECRET = "174jzh9s0ik24h5"
BASE_URL = "https://8000-boyuan12-classroom-7wpk4b33gw2.ws-us47.gitpod.io"

def dropbox_oauth(request):
    return redirect(f"https://www.dropbox.com/oauth2/authorize?client_id={DROPBOX_APP_KEY}&redirect_uri={BASE_URL}/dropbox/authorized&response_type=code")

def dropbox_authorized(request):
    code = request.GET["code"]
    data = requests.post("https://api.dropboxapi.com/oauth2/token", data={
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": f"{BASE_URL}/dropbox/authorized",
    }, auth=(DROPBOX_APP_KEY, DROPBOX_APP_SECRET))
    request.session["DROPBOX_ACCESS_TOKEN"] = data.json()["access_token"]
    return redirect("/dropbox/search")

def search_files(request):
    if request.method == "GET":
        return render(request, "dropbox/search.html")

def selected_file(request, file_id):
    data = requests.post("https://content.dropboxapi.com/2/files/download", headers={
        'Authorization': f'Bearer {request.session["DROPBOX_ACCESS_TOKEN"]}',
        "Dropbox-API-Arg": json.dumps({"path": file_id})
    }, stream=True)
    print(json.loads(dict(data.headers)["Dropbox-Api-Result"])["name"])
    name = json.loads(dict(data.headers)["Dropbox-Api-Result"])["name"]
    # name = dict(data.headers["Dropbox-Api-Result"]["name"])
    r = cloudinary.uploader.upload(data.content, resource_type="raw")
    url = r["secure_url"]
    return redirect(f"/classroom/{request.session['previous_classroom_code']}/assignment/{request.session['previous_assignment_slug']}/?dropbox_url={url}?dropbox_file_name={name}")

@csrf_exempt
def search_files_api(request):
    query = request.GET["query"]

    data = requests.post("https://api.dropboxapi.com/2/files/search_v2", headers={
        'Authorization': f'Bearer {request.session["DROPBOX_ACCESS_TOKEN"]}'
    }, json={
        "query": query
    })

    results = [] # [[id, filename, prev_url]]

    for f in data.json()["matches"]:
        id = f["metadata"]["metadata"]["id"]
        data = requests.post("https://content.dropboxapi.com/2/files/get_preview", headers={
            'Authorization': f'Bearer {request.session["DROPBOX_ACCESS_TOKEN"]}',
            'Dropbox-API-Arg': json.dumps({
                "path": id
            })
        }, stream=True)

        r = cloudinary.uploader.upload(data.content)
        pdf_url = r["secure_url"]
        prev_url = convert_file(pdf_url, "png")
        filename = f["metadata"]["metadata"]["name"]

        results.append([id, filename, prev_url])

    return JsonResponse(results, safe=False)
    # return JsonResponse(data.json())

