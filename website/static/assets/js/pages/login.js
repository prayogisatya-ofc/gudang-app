$(document).ready(function(){
    $('#btnLogin').on("click", function(){
        var user = $("#username").val(),
        pass = $("#password").val()
        
        if(user || pass){
            $.ajax({
                headers:{"X-CSRFToken":token},
                type:"POST",
                url:"/login/",
                data:{
                    "username":user,
                    "password":pass
                },
                dataType:"json"
            }).done(a=>{
                if (a.status){
                    Swal.fire({
                        icon: 'success',
                        text: 'Berhasil login',
                        showConfirmButton: false,
                        timer: 2000
                    }).then(a=>{
                        window.location.href="/"
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