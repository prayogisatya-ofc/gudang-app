from django.shortcuts import render, redirect
from .. import models as db
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

def controller(request):
    return redirect('/') if request.session.get('user') else views(request) if request.method == 'GET' else ajax(request)

def views(request):
    return render(request, 'view/login.html')

def ajax(request):
    result = {
        "status": False
    }

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        query = db.User.objects.filter(username=username)
        if query.exists():
            check = check_password(password, query[0].password)
            if check:
                result['status'] = check
                request.session['user'] = query[0].id
                request.session['role'] = query[0].role
            else:
                result['message'] = 'Password anda salah!'
        else:
            result['message'] = 'Username tidak di temukan!'

    return JsonResponse(result)