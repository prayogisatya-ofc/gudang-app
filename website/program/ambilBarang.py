from django.shortcuts import render, redirect
from .. import models as db
from django.http import JsonResponse, HttpResponse
import datetime

def controller(request):
    return redirect('/login/') if not request.session.get('user') else views(request) if request.method == 'GET' else ajax(request)

def views(request):
    user = db.User.objects.get(id=request.session.get('user'))
    barang = db.Barang.objects.all()

    context = {
        "auth": user,
        "barang": barang,
    }
    return render(request, 'view/ambilBarang.html', context=context)

def ajax(request):
    result = {
        "status": False
    }

    if request.session.get('user') and request.session.get('role') != 'owner':
        if request.POST:
            barang = request.POST.get('barang')
            stok = int(request.POST.get('stok'))
            tanggal = request.POST.get('tanggal')
            pengambil = request.POST.get('pengambil')
            if stok and tanggal and pengambil:
                query = db.Barang.objects.filter(id=barang)
                if stok != 0:
                    if stok > query[0].get_stok():
                        result['message'] = "Stok keluar tidak boleh lebih dari '"+query[0].get_stok()+"'!"
                    else:
                        db.BarangKeluar(
                            barang=query[0],
                            stok=stok,
                            pengambil=pengambil,
                            waktu=tanggal
                        ).save()
                        result['status'] = True
                else:
                    result['message'] = "Stok tidak boleh '0'!"
            else:
                result['message'] = "Ada form yang masih kosong!"

    return JsonResponse(result)