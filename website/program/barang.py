from django.shortcuts import render, redirect
from .. import models as db
from django.http import JsonResponse, HttpResponse
import pandas as pd
import datetime

def controller(request):
    return redirect('/login/') if not request.session.get('user') else views(request) if request.method == 'GET' else ajax(request)

def views(request):
    barangs = db.Barang.objects.all()
    user = db.User.objects.get(id=request.session.get('user'))

    context = {
        "barangs": barangs,
        "auth": user
    }
    return render(request, 'view/barang.html', context=context)

def ajax(request):
    result = {
        "status": False
    }

    if request.session.get('user') and request.session.get('role') != 'owner':
        if request.POST:
            nama = request.POST.get('nama')
            pemasok = request.POST.get('pemasok')
            fungsi = request.POST.get('fungsi')
            idb = request.POST.get('id')
            if nama and pemasok:
                query = db.Barang.objects.filter(id=idb)
                query.update(
                    nama=nama,
                    pemasok=pemasok,
                    fungsi=fungsi
                )
                result['status'] = True
            else:
                result['message'] = "Ada form yang masih kosong!"

    return JsonResponse(result)

def hapus(request):
    result = {
        "status": False
    }

    if request.session.get('user') and request.session.get('role') != 'owner':
        if request.POST:
            idb = request.POST.get('id')
            query = db.Barang.objects.filter(id=idb)
            if query.exists():
                query[0].delete()
                result['status'] = True
            else:
                result['message'] = "Data tidak tersedia!"

    return JsonResponse(result)

def printData(request):
    if request.session.get('user'):
        barangs = db.Barang.objects.all()

        context = {
            "barangs": barangs
        }
        return render(request, 'print/barang.html', context=context)

def exportData(request):
    objs = db.Barang.objects.all()
    data = []

    for obj in objs:
        data.append({
            "nama_barang": obj.nama,
            "stok_barang": obj.get_stok(),
            "pemasok": obj.pemasok,
            "fungsi_barang": obj.fungsi
        })
    date = datetime.datetime.today()
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="data-barang-'+date.strftime('%d-%m-%Y')+'.xlsx"'                                        
    df.to_excel(response)
    return response