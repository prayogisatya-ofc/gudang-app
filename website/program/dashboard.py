from django.shortcuts import render, redirect
from .. import models as db
from django.http import JsonResponse

def controller(request):
    return redirect('/login/') if not request.session.get('user') else views(request) if request.method == 'GET' else ajax(request)

def views(request):
    user = db.User.objects.get(id=request.session.get('user'))
    barang = db.Barang.objects.all().count()
    barangM = db.BarangMasuk.objects.all().count()
    barangK = db.BarangKeluar.objects.all().count()
    users = db.User.objects.all().count()

    context = {
        "auth": user,
        "barang":barang,
        "barangM":barangM,
        "barangK":barangK,
        "user":users,
    }
    return render(request, 'view/dashboard.html', context=context)

def ajax(request):
    try:
        del request.session['user']
        del request.session['role']
        return JsonResponse({
            "status": True,
            "message": "Berhasil logout"
        })
    except:
        return JsonResponse({
            "status": False,
            "message": "Telah logout"
        })