
var arr_no_box_besar = [];
var arr_rincian = [];
$(function() {
    changePetugas();
    $('.select2').select2();

    $("select[id=kd_kab]").on("change", function() {
        changeNoBoxBesar();
        changePetugas();
    })

    $("button[name=add_wilayah]").on("click", function(e) {
        e.preventDefault();
        var kd_prop = "33";
        var kd_kab = $("select[id=kd_kab]").val();
        var no_box_besar = $("select[id=no_box_besar]").val();
        console.log(no_box_besar)
        if (kd_kab == "" || no_box_besar == "" || no_box_besar == null) {
            Swal.fire("Gagal", "Pilih wilayah terlebih dahulu", "error");
        } else {

            if (!arr_no_box_besar.includes(no_box_besar)) {
                Swal.fire({
                    title: "Loading...",
                    text: "Please wait",
                    // imageUrl: "https://sipmen.bps.go.id/st2023/public/images/Pulse-1s-200px.gif",
                    showConfirmButton: false,
                    allowOutsideClick: false,
                    onOpen: () => {
                        swal.showLoading();
                    }
                });
                $.ajax({
                    headers: {
                        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                    },
                    // url: '/sipmen-kirim-ke-prop/load-rincian-no-box-besar',
                    url: "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/load-rincian-no-box-besar",
                    //url: "https://sipmen.bps.go.id/st2023/sipmen-kirim-ke-prop/load-rincian-no-box-besar",
                    method: "GET",
                    data: {
                        no_box_besar: no_box_besar,
                        kd_prop: '33'
                    },
                }).done(function(response) {
                    arr_no_box_besar.push(no_box_besar);
                    arr_rincian.push(response.data);
                    list_wilayah();
                    Swal.close();
                }).fail(function(jqXHR, textStatus) {
                    Swal.close();
                });

            }
        }
    });

    $("#simpan1").on("click", function(e) {
        e.preventDefault();
        var no_surat = $("#no_surat").val();
        var no_box_besar = arr_no_box_besar.join("*");
        var petugas = $("select[id=petugas]").val();
        if (no_surat == '') {
            $("div[id=str_error]").html(
                "<div class=\'alert alert-danger\'>Isikan data yang kosong</div>");
            console.log('if1', wilayah);
        } else if (no_box_besar == '') {
            $("div[id=str_error]").html("<div class=\'alert alert-danger\'>Isikan No Batch</div>");
        } else {
            $("#simpan1").attr('disabled', 'disabled'); // disable
            // console.log('test',wilayah);
            $.ajax({
                headers: {
                    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                },
                url: "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/insert_surat",
                data: {
                    'no_surat': no_surat,
                    'no_box_besar': no_box_besar,
                    'petugas': petugas
                },
                type: 'post',
                success: function(response) {
                    var obj = JSON.parse(response);
                    $("#simpan1").removeAttr('disabled');
                    if (obj['status'] == 'gagal') {
                        $("div[id=str_error]").html(
                            "<div class=\'alert alert-danger\'>" + obj['ket'] +
                            "</div>");
                    } else if (obj['status'] == 'berhasil') {
                        var url =
                            "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/index-generate-box-kab";
                        window.location = url;
                    }
                }
            });
        }
    });
})


function changeNoBoxBesar() {
    $("select[id=no_box_besar]").html("<option value=''>Pilih No Batch</option>");
    if ($("select[id=kd_kab]").val() != "") {
        $.ajax({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            },
            // url: '/sipmen-kirim-ke-prop/load-no-box-besar', 
            url: "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/load-noboxbesar",
            //url: "https://sipmen.bps.go.id/st2023/sipmen-kirim-ke-prop/load-no-box-besar",
            method: "GET",
            data: {
                kd_kab: $("select[id=kd_kab]").val(),
                kd_prop: '33'
            },
        }).done(function(response) {
            $('select[id=no_box_besar]').prop('disabled', false);
            $("select[id=no_box_besar]").html(response.data);
        }).fail(function(jqXHR, textStatus) {

        });
    }
}

function changePetugas() {
    $("select[id=petugas]").html("<option value=''>Pilih Petugas</option>");
    if ($("select[id=kd_kab]").val() != "") {
        $.ajax({
            headers: {
                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
            },
            url: "https://sipmen.bps.go.id/st2023/petugas/load-petugas",
            method: "POST",
            data: {
                kd_kab: $("select[id=kd_kab]").val(),
                kd_prop: '33',
                tahap: '3'
            },
        }).done(function(response) {
            $("select[id=petugas]").html(response);
        }).fail(function(jqXHR, textStatus) {

        });
    }
}

function remove_wilayah(index) {
    arr_no_box_besar.splice(index, 1);
    arr_rincian.splice(index, 1);
    list_wilayah();
}

function list_wilayah() {
    $("table[name=list_wilayah]").html("");
    var html = "";
    for (var i = 0, l = arr_no_box_besar.length; i < l; i++) {
        html += '<tr>';
        html += '<td rowspan="' + (arr_rincian[i].length + 1) +
            '" style="text-align:left"><a href="javascript:remove_wilayah(' + i +
            ')"><i class="fa fa-fw fa-times" style="color: red"></i></a>' + '</td>';
        html += '<td rowspan="' + (arr_rincian[i].length + 1) + '">' + arr_no_box_besar[i] + '</td>';
        html += '</tr>';
        // for (var j = 0, k = arr_rincian[i].length; j < k; j++){
        //     html += '<tr>';
        //     html += '<td>';
        //     html +=  arr_rincian[i][j]["wilayah"]
        //     html += '</td>';
        //     html += '</tr>';
        // }                       
    }
    $("table[name=list_wilayah]").append(html);
}
