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

    $('#btnSimpan').on('click',function(){
        const nama = $('#nama').val(),
        username = $('#username').val(),
        password = $('#password').val(),
        role = $("#role option:selected").attr("value")

        if(nama && username && password && role){
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
                        url:"/petugas/",
                        data:{
                            "nama":nama,
                            "username":username,
                            "password":password,
                            "role":role
                        },
                        dataType:"json"
                    }).done(a=>{
                        if (a.status){
                            Swal.fire({
                                icon: 'success',
                                text: 'Berhasil tambah petugas',
                                showConfirmButton: false,
                                timer: 2000
                            }).then(a=>{
                                window.location.href="/petugas/"
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
                text: 'Ada form yang belum diisi!',
                showConfirmButton: false,
                timer: 2000
            })
        }
    })
})