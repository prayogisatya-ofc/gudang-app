$(document).ready(function(){
    $('[data-toggle="touchspin"]').TouchSpin()
    $('[data-plugin="customselect"]').select2()

    $('#btnSimpan').on('click', function(){
        const barang = $('#barangK option:selected').attr('value'),
        pengambil = $('#pengambilK').val(),
        tanggal = $('#tanggalK').val(),
        stokSisa = $('#stokFix').text(),
        stok = $('#stokK').val()

        console.log(stok);
        console.log(stokSisa);

        if(stok && tanggal && pengambil && barang){
            if (stok != 0) {
                if (stok > parseInt(stokSisa)) {
                    Swal.fire({
                        icon: 'warning',
                        text: 'Stok keluar tidak boleh lebih dari "'+stokSisa+'"!',
                        showConfirmButton: false,
                        timer: 2000
                    })
                } else {
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
                                url:"/ambil-barang/",
                                data:{
                                    "barang":barang,
                                    "stok":stok,
                                    "tanggal":tanggal,
                                    "pengambil":pengambil
                                },
                                dataType:"json"
                            }).done(a=>{
                                if (a.status){
                                    Swal.fire({
                                        icon: 'success',
                                        text: 'Berhasil tambah barang keluar',
                                        showConfirmButton: false,
                                        timer: 2000
                                    }).then(a=>{
                                        window.location.href="/barang-keluar/"
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
                }
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
    })
})