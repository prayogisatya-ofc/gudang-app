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
    
    barangs = db.BarangMasuk.objects.filter(waktu__range=[times['start'], times['end']])

    context = {
        "barangs": barangs,
        "auth": user,
        "masuk": barang,
        "start":times['start'],
        "end":times['end']
    }
    return render(request, 'view/barang_masuk.html', context=context)

def ajax(request):
    result = {
        "status": False
    }

    if request.session.get('user') and request.session.get('role') != 'owner':
        if request.POST:
            barang = request.POST.get('barang')
            stok = int(request.POST.get('stok'))
            tanggal = request.POST.get('tanggal')
            if barang and stok and tanggal:
                if stok != 0:
                    query = db.Barang.objects.filter(id=barang)
                    db.BarangMasuk(
                        barang=query[0],
                        stok=stok,
                        penerima=db.User.objects.get(id=request.session.get('user')),
                        waktu=tanggal
                    ).save()
                    result['status'] = True
                else:
                    result['message'] = "Stok tidak boleh '0'!"
            else:
                result['message'] = "Ada form yang masih kosong!"

    return JsonResponse(result)

def tambah(request):
    result = {
        "status": False
    }

    if request.session.get('user') and request.session.get('role') != 'owner':
        if request.POST:
            barang = request.POST.get('barang')
            stok = int(request.POST.get('stok'))
            pemasok = request.POST.get('pemasok')
            fungsi = request.POST.get('fungsi')
            tanggal = request.POST.get('tanggal')
            if barang and stok and pemasok and tanggal:
                if stok != 0:
                    query = db.Barang(
                        nama=barang,
                        pemasok=pemasok,
                        fungsi=fungsi
                    )
                    query.save()
                    print(query)
                    db.BarangMasuk(
                        barang=query,
                        stok=stok,
                        penerima=db.User.objects.get(id=request.session.get('user')),
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
            barang = request.POST.get('barang')
            stok = int(request.POST.get('stok'))
            tanggal = request.POST.get('tanggal')
            idb = request.POST.get('id')
            if barang and stok and tanggal:
                if stok != 0:
                    query = db.Barang.objects.filter(id=barang)
                    db.BarangMasuk.objects.filter(id=idb).update(
                        barang=query[0],
                        stok=stok,
                        waktu=tanggal
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
            query = db.BarangMasuk.objects.filter(id=idb)
            if query.exists():
                query[0].delete()
                result['status'] = True
            else:
                result['message'] = "Data tidak tersedia!"

    return JsonResponse(result)

def printData(request, start, end):
    if request.session.get('user'):
        barangs = db.BarangMasuk.objects.filter(waktu__range=[start, end])

        context = {
            "barangs": barangs,
            "start": datetime.datetime.strptime(start, '%Y-%m-%d'),
            "end":datetime.datetime.strptime(end, '%Y-%m-%d')
        }
        return render(request, 'print/barang_masuk.html', context=context)

def exportData(request, start, end):
    objs = db.BarangMasuk.objects.filter(waktu__range=[start, end])
    data = []

    for obj in objs:
        data.append({
            "nama_barang": obj.barang.nama,
            "stok_barang_masuk": obj.stok,
            "pemasok": obj.barang.pemasok,
            "penerima_barang": obj.penerima.nama,
            "tanggal_penerimaan": obj.waktu
        })
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="data-barang-masuk-'+start+'-sampai-'+end+'.xlsx"'                                        
    df.to_excel(response)
    return response