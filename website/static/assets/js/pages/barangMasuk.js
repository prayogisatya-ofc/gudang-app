$(document).ready(function(){
    $("#basic-datatable").DataTable({
        language:{
            paginate:{
                previous:"<i class='uil uil-angle-left'>",
                next:"<i class='uil uil-angle-right'>"
            }
        },
        drawCallback:function(){
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded")
        }
    });

    $('[data-plugin="customselect"]').select2({
        tags:true
    })
    $('[data-toggle="touchspin"]').TouchSpin()

    $('#barangSA').on('change', function(){
        $('#box-btn-simpan').removeClass('d-none')

        if ($('#barangSA option:selected').attr('data-select2-tag')) {
            $('#box-form').html(`
            <div class="form-group">
                <label>Pemasok</label>
                <input type="text" class="form-control" id="pemasokSA">
            </div>
            `)
        } else {
            $('#box-form').html(``)
        }
    })


    $('#btnSimpan').on('click',function(){
        const barang = $("#barangSA").val(),
        stok = $('#stokSA').val(),
        tanggal = $('#tanggalSA').val()

        if($('#pemasokSA').length == 1){
            const pemasok = $('#pemasokSA').val()

            if(barang && stok && tanggal && pemasok){
                if (stok != 0) {
                    Swal.fire({
                        icon: 'warning',
                        text: 'Apakah anda yakin data yang dimasukkan sudah benar?',
                        showCancelButton: true,
                        cancelButtonText: "Belum",
                        confirmButtonText: "Yakin",
                        confirmButtonColor: "#5369F8",
                    }).then((r)=>{
                        if(r.isConfirmed){
                            $.ajax({
                                headers:{"X-CSRFToken":token},
                                type:"POST",
                                url:"/barang-masuk/",
                                data:{
                                    "barang":barang,
                                    "stok":stok,
                                    "tanggal":tanggal,
                                    "pemasok": pemasok
                                },
                                dataType:"json"
                            }).done(a=>{
                                if (a.status){
                                    Swal.fire({
                                        icon: 'success',
                                        text: 'Berhasil tambah barang masuk',
                                        showConfirmButton: false,
                                        timer: 2000
                                    }).then(a=>{
                                        window.location.href="/barang-masuk/"
                                    })
                                } else {
                                    Swal.fire({
                                        icon: 'error',
                                        text: a.message,
                                        showConfirmButton: false,
                                        timer: 2000
                                    })
                                }
                            })
                        }
                    })
                } else {
                    Swal.fire({
                        icon: 'warning',
                        text: 'Stok tidak boleh "0"!',
                        showConfirmButton: false,
                        timer: 2000
                    })
                }
            } else {
                Swal.fire({
                    icon: 'warning',
                    text: 'Ada form yang belum diisi!',
                    showConfirmButton: false,
                    timer: 2000
                })
            }
        } else {
            if(barang && stok && tanggal){
                if (stok != 0) {
                    Swal.fire({
                        icon: 'warning',
                        text: 'Apakah anda yakin data yang dimasukkan sudah benar?',
                        showCancelButton: true,
                        cancelButtonText: "Belum",
                        confirmButtonText: "Yakin",
                        confirmButtonColor: "#5369F8",
                    }).then((r)=>{
                        if(r.isConfirmed){
                            $.ajax({
                                headers:{"X-CSRFToken":token},
                                type:"POST",
                                url:"/barang-masuk/",
                                data:{
                                    "barang":barang,
                                    "stok":stok,
                                    "tanggal":tanggal
                                },
                                dataType:"json"
                            }).done(a=>{
                                if (a.status){
                                    Swal.fire({
                                        icon: 'success',
                                        text: 'Berhasil tambah barang masuk',
                                        showConfirmButton: false,
                                        timer: 2000
                                    }).then(a=>{
                                        window.location.href="/barang-masuk/"
                                    })
                                } else {
                                    Swal.fire({
                                        icon: 'error',
                                        text: a.message,
                                        showConfirmButton: false,
                                        timer: 2000
                                    })
                                }
                            })
                        }
                    })
                } else {
                    Swal.fire({
                        icon: 'warning',
                        text: 'Stok tidak boleh "0"!',
                        showConfirmButton: false,
                        timer: 2000
                    })
                }
            } else {
                Swal.fire({
                    icon: 'warning',
                    text: 'Ada form yang belum diisi!',
                    showConfirmButton: false,
                    timer: 2000
                })
            }
        }

    })
})