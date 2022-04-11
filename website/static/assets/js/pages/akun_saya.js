$(document).ready(function(){
    $('#btnSimpan').on('click', function(){
        const nama = $('#nama').val(),
        username = $('#username').val(),
        password = $('#password').val()

        if(nama && username && password ){
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
                            url:"/akun-saya/",
                            data:{
                                "nama":nama,
                                "username":username,
                                "password":password,
                            },
                            dataType:"json"
                        }).done(a=>{
                            if (a.status){
                                Swal.fire({
                                    icon: 'success',
                                    text: 'Berhasil ubah akun saya',
                                    showConfirmButton: false,
                                    timer: 2000
                                }).then(a=>{
                                    window.location.href="/akun-saya/"
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