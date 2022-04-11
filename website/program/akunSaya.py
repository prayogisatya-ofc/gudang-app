from django.shortcuts import render, redirect
from .. import models as db
from django.http import JsonResponse, HttpResponse
import xlwt
from django.contrib.auth.hashers import make_password

def controller(request):
    return redirect('/login/') if not request.session.get('user') else views(request) if request.method == 'GET' else ajax(request)

def views(request):
    petugases = db.User.objects.get(id=request.session.get('user'))
    user = db.User.objects.get(id=request.session.get('user'))
    context = {
        "petugases": petugases,
        "auth": user
    }
    return render(request, 'view/akun_saya.html', context=context)

def ajax(request):
    result = {
        "status": False
    }

    if request.POST:
        nama = request.POST.get('nama')
        username = request.POST.get('username')
        password = request.POST.get('password')
        passw = make_password(password, hasher="pbkdf2_sha256")
        if nama and username and password:
            user = db.User.objects.filter(id=request.session.get('user'))
            if user.exists():
                if not db.User.objects.filter(username=username).exclude(id=user[0].id).exists():
                    user.update(
                        nama=nama,
                        username=username,
                        password=passw,
                    )
                    result['status'] = True
                else:
                    result['message'] = "Username sudah ada!"
            else:
                result['message'] = "Data tidak ada!"
        else:
            result['message'] = "Ada form yang masih kosong!"

    return JsonResponse(result)