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

    $('[data-plugin="customselect"]').select2()
    $('[data-toggle="touchspin"]').TouchSpin()
})