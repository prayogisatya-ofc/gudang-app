from django.shortcuts import render, redirect
from .. import models as db
from django.http import JsonResponse, HttpResponse
import xlwt
import numpy as np
from django.contrib.auth.hashers import make_password

def controller(request):
    if request.session.get('user') and request.session.get('role') == 'admin':
        if request.method == "POST":
            return ajax(request)
        return views(request)
    else:
        return redirect('/login/')

def views(request):
    petugases = db.User.objects.exclude(id=request.session.get('user'))
    user = db.User.objects.get(id=request.session.get('user'))
    role = {
        'admin',
        'owner',
        'officer'
    }
    context = {
        "petugases": petugases,
        "auth": user,
        "role":role
    }
    return render(request, 'view/petugas.html', context=context)

def ajax(request):
    result = {
        "status": False
    }

    if request.POST:
        nama = request.POST.get('nama')
        username = request.POST.get('username')
        password = request.POST.get('password')
        passw = make_password(password, hasher="pbkdf2_sha256")
        role = request.POST.get('role')
        if nama and username and password and role:
            query = db.User.objects.filter(username=username)
            if query.exists():
                result['message'] = "Username sudah digunakan!"
            else:
                db.User(
                    nama=nama,
                    username=username,
                    password=passw,
                    role=role
                ).save()
                result['status'] = True
        else:
            result['message'] = "Ada form yang masih kosong!"

    return JsonResponse(result)

def update(request):
    result = {
        "status": False
    }

    if request.session.get('user') and request.session.get('role') == 'admin':
        if request.POST:
            nama = request.POST.get('nama')
            username = request.POST.get('username')
            password = request.POST.get('password')
            passw = make_password(password, hasher="pbkdf2_sha256")
            role = request.POST.get('role')
            idp = request.POST.get('id')
            if nama and username and password and role:
                user = db.User.objects.filter(id=idp)
                if user.exists():
                    if db.User.objects.filter(username=username).exclude(id=idp).exists():
                        result['message'] = "Username sudah digunakan!"
                    else:
                        user.update(
                            nama=nama,
                            username=username,
                            password=passw,
                            role=role
                        )
                        result['status'] = True
                else:
                    result['message'] = "Data tidak ada!"
            else:
                result['message'] = "Ada form yang masih kosong!"

    return JsonResponse(result)

def hapus(request):
    result = {
        "status": False
    }
    
    if request.session.get('user') and request.session.get('role') == 'admin':
        if request.POST:
            idb = request.POST.get('id')
            query = db.User.objects.filter(id=idb)
            if query.exists():
                query[0].delete()
                result['status'] = True
            else:
                result['message'] = "Data tidak tersedia!"

    return JsonResponse(result)