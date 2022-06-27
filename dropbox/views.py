from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import requests
import json

import cloudinary
import cloudinary.uploader
import cloudinary.api
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
    return JsonResponse(data.json())

def search_files(request):
    data = requests.post("https://api.dropboxapi.com/2/files/search_v2", headers={
        'Authorization': f'Bearer {request.session["DROPBOX_ACCESS_TOKEN"]}'
    }, json={
        "query": "dwm"
    })

    results = []

    for f in data.json()["matches"]:
        id = f["metadata"]["metadata"]["id"]
        data = requests.post("https://content.dropboxapi.com/2/files/get_preview", headers={
            'Authorization': f'Bearer {request.session["DROPBOX_ACCESS_TOKEN"]}',
            'Dropbox-API-Arg': json.dumps({
                "path": id
            })
        }, stream=True)

        print(data.text)
        r = cloudinary.uploader.upload(data.content)
        img_url = r["secure_url"]
        
        return HttpResponse(img_url)

    # return JsonResponse(data.json())