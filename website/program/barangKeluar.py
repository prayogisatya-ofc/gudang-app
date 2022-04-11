from django.shortcuts import render, redirect
from .. import models as db
from django.http import JsonResponse, HttpResponse
import datetime
import pandas as pd

def controller(request):
    return redirect('/login/') if not request.session.get('user') else views(request) if request.method == 'GET' else ajax(request)

def views(request):
    user = db.User.objects.get(id=request.session.get('user'))
    barang = db.Barang.objects.all()

    if request.GET.get('start') and request.GET.get('end'):
        times = {
            "start": datetime.datetime.strptime(request.GET.get('start'), '%Y-%m-%d'),
            "end": datetime.datetime.strptime(request.GET.get('end'), '%Y-%m-%d')
        }
    else:
        times = {
            "start": datetime.datetime.today() - datetime.timedelta(days=10),
            "end": datetime.datetime.today() + datetime.timedelta(days=1)
        }
    
    barangs = db.BarangKeluar.objects.filter(waktu__range=[times['start'], times['end']])

    for i in range(len(barangs)):
        barangs[i].stokSisa = barangs[i].stok + barangs[i].barang.get_stok()

    context = {
        "barangs": barangs,
        "auth": user,
        "masuk": barang,
        "start":times['start'],
        "end":times['end']
    }
    return render(request, 'view/barang_keluar.html', context=context)

def ajax(request):
    result = {
        "status": False
    }

    if request.session.get('user') and request.session.get('role') != 'owner':
        if request.POST:
            idb = request.POST.get('id')
            stok = int(request.POST.get('stok'))
            tanggal = request.POST.get('tanggal')
            pengambil = request.POST.get('pengambil')
            if stok and tanggal and pengambil:
                query = db.Barang.objects.filter(id=idb)
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

def update(request):
    result = {
        "status": False
    }

    if request.session.get('user') and request.session.get('role') != 'owner':
        if request.POST:
            stok = int(request.POST.get('stok'))
            tanggal = request.POST.get('tanggal')
            pengambil = request.POST.get('pengambil')
            idb = request.POST.get('id')
            if stok and tanggal and pengambil:
                query = db.BarangKeluar.objects.filter(id=idb)
                stokSiswa = query[0].stok + query[0].barang.get_stok()
                if stok != 0:
                    if stok > stokSiswa:
                        result['message'] = "Stok keluar tidak boleh lebih dari '"+query[0].barang.get_stok()+"'"
                    else:
                        query.update(
                            stok=stok,
                            waktu=tanggal,
                            pengambil=pengambil
                        )
                        result['status'] = True
                else:
                    result['message'] = "Stok tidak boleh '0'!"
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
            query = db.BarangKeluar.objects.filter(id=idb)
            if query.exists():
                query[0].delete()
                result['status'] = True
            else:
                result['message'] = "Data tidak tersedia!"

    return JsonResponse(result)

def printData(request, start, end):
    if request.session.get('user'):
        barangs = db.BarangKeluar.objects.filter(waktu__range=[start, end])

        context = {
            "barangs": barangs,
            "start": datetime.datetime.strptime(start, '%Y-%m-%d'),
            "end":datetime.datetime.strptime(end, '%Y-%m-%d')
        }
        return render(request, 'print/barang_keluar.html', context=context)

def exportData(request, start, end):
    objs = db.BarangKeluar.objects.filter(waktu__range=[start, end])
    data = []

    for obj in objs:
        data.append({
            "nama_barang": obj.barang.nama,
            "stok_barang_masuk": obj.stok,
            "pemasok": obj.barang.pemasok,
            "pengambil_barang": obj.pengambil,
            "tanggal_pengambilan": obj.waktu
        })
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="data-barang-keluar-'+start+'-sampai-'+end+'.xlsx"'                                        
    df.to_excel(response)
    return response