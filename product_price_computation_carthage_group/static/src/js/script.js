var d2 = document.getElementById('d2').value
var d1 = document.getElementById('d1').value
var d3 = document.getElementById('d3').value
$('#d1').datepicker();
$('#d1').datepicker("option", "dateFormat", "yy-mm-dd");
$('#d1').datepicker("setDate", d1);
$('#d2').datepicker();
$('#d2').datepicker("option", "dateFormat", "yy-mm-dd");
$('#d2').datepicker("setDate", d2);


// function setpicker(id){
//     var iddiv = '#dates-div-' + id
//     var idstr = $(iddiv).find('input')
//
//     idstr.datepicker();
//     idstr.datepicker( "option", "dateFormat", "yy-mm-dd" );
// }


function hide(id) {
    var strdates = '#dates_create-' + id
    var strperiod = '#periods_ready-' + id
    if ($(strdates).is(":visible")) {
        // alert('going to hide dates'+ $(this).is(":checked"))
        $(strdates).hide();
        $(strperiod).show();


    } else {
        // alert('going to show dates' + $(this).is(":checked"))
        $(strdates).show();
        $(strperiod).hide();
    }
}

function toastit(id1, d, mdl_name, id_h) {
    $('.toast').toast('show', {
        'delay': 5000,
        'autohide': false
    })
    // var idelmnt = this.getAttribute('id');
    var x = id1;
    var y = document.querySelectorAll('.buttons_wrapper1')
    var mdll = mdl_name.split(".")
    $("[value=" + id1 + "]")['0'].style.display = 'none';
    document.cookie = "copy=" + x + "";
    $('.buttons_wrapper1').append('<button id="paste_button1" type="button"\n' +
        '                   value="' + x + '"                                         ' +
        ' class="btn btn-light"\n' +
        'data-toggle="tooltip" data-placement="top" title="' + d + '"' +
        '                                                                                onclick="coller(' + x + ',this)"\n' +
        '                                                                        >\n' +
        '                                                                            <i class="fas fa-paste"></i>\n' +
        '                                                                        </button>');
    for (var iter = 2; iter < $("[id=" + id_h + "]")['0'].children[1].children.length; iter++) {

        $("[id=" + id_h + "]")['0'].children[1].children[iter].style.display = 'none';
    }
}

function toastit_spo(id1, d, mdl_name, id_h) {
    $('.toast').toast('show', {
        'delay': 5000,
        'autohide': false
    })
    // var idelmnt = this.getAttribute('id');
    var x = id1;
    var mdll = mdl_name.split(".")
    $("[value=" + id1 + "]")['0'].style.display = 'none';
    document.cookie = "copy=" + x + "";
    $('.buttons_wrapper1').append('<button id="paste_button1" type="button"\n' +
        '                   value="' + x + '"                                         ' +
        ' class="btn btn-success"\n' +
        'data-toggle="tooltip" data-placement="top" title="' + d + '"' +
        '                                                                                onclick="coller_spo(' + x + ',this)"\n' +
        '                                                                        >\n' +
        '                                                                            <i class="fas fa-paste"></i>\n' +
        '                                                                        </button>');
    for (var iter = 2; iter < $("[id=" + id_h + "]")['0'].children[1].children.length; iter++) {

        $("[id=" + id_h + "]")['0'].children[1].children[iter].style.display = 'none';
    }

}

function coller(inte, b) {
    $('#' + inte).clone().appendTo(b.parentNode.parentNode.firstElementChild.children[1])
    var data = [];
    var id_copier = inte;
    var y = b.parentNode.parentNode.getAttribute("id")
    var model_name_p = $('#' + b.parentNode.parentNode.getAttribute("id")).find('#model_name')[0].value
    var model_name_c = $('#' + inte).parent().parent().find('#model_name').val()
    data = $.ajax({
        type: "GET", //rest Type
        dataType: 'jsonp', //mispelled
        url: 'http://' + window.location.hostname + '/matrix/copy_price?id_copy=' + inte + '&id_paste=' + y + '&model_name_paste=' + model_name_p + '&model_name_copy=' + model_name_c,
        async: false,

        success: function (msg) {
            console.log(this.responseText);
        }
    }).responseText;

}

function coller_spo(inte, b) {
    $('#' + inte).clone().appendTo(b.parentNode.parentNode.firstElementChild.children[2])
    var data = [];
    var id_copier = inte;
    var y = b.parentNode.parentNode.getAttribute("id")
    var model_name_p = $('#' + b.parentNode.parentNode.getAttribute("id")).find('#model_name')[0].value
    var model_name_c = $('#' + inte).parent().parent().find('#model_name').val()
    data = $.ajax({
        type: "GET", //rest Type
        dataType: 'jsonp', //mispelled
        url: 'http://' + window.location.hostname + '/matrix/copy_spo?id_copy=' + inte + '&id_paste=' + y + '&model_name_paste=' + model_name_p + '&model_name_copy=' + model_name_c,
        async: false,

        success: function (msg) {
            console.log(this.responseText);
        }
    }).responseText;

}


$(document).ready(function () {
    $("#search_hotel").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#accordionExample li").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

$(function () {
    $("#slider-range").slider({
        range: true,
        min: 12,
        max: 99,
        values: [12, 99],
        slide: function (event, ui) {
            $("#amount").val("" + ui.values[0] + " - " + ui.values[1]);
        }
    });
    $("#amount").val("" + $("#slider-range").slider("values", 0) +
        " - " + $("#slider-range").slider("values", 1));
});
$(function () {
    $("#slider-range1").slider({
        range: true,
        min: 2,
        max: 12,
        values: [2, 12],
        slide: function (event, ui) {
            $("#amount1").val("" + ui.values[0] + " - " + ui.values[1]);
        }
    });
    $("#amount1").val("" + $("#slider-range1").slider("values", 0) +
        " - " + $("#slider-range1").slider("values", 1));
});
$(function () {
    $("#slider-range2").slider({
        range: true,
        min: 0,
        max: 2,
        values: [0, 2],
        slide: function (event, ui) {
            $("#amount2").val("" + ui.values[0] + " - " + ui.values[1]);
        }
    });
    $("#amount2").val("" + $("#slider-range2").slider("values", 0) +
        " - " + $("#slider-range2").slider("values", 1));
});


$("#amount").change(function () {
    st = document.getElementById("amount").value
    res = st.split(" - ")
    borne1 = res[0]
    borne2 = res[1]
    if (parseInt(borne1, 10) > parseInt(borne2, 10)) {
        alert('first value cant  be bigger then the second value')
    } else {

        $("#slider-range").slider("values", 0, res[0])
        $("#slider-range").slider("values", 1, res[1])
    }

})
$("#amount1").change(function () {
    st = document.getElementById("amount1").value
    res = st.split(" - ")
    borne1 = res[0]
    borne2 = res[1]
    if (parseInt(borne1, 10) > parseInt(borne2, 10)) {
        alert('first value cant  be bigger then the second value')
    } else {

        $("#slider-range1").slider("values", 0, res[0])
        $("#slider-range1").slider("values", 1, res[1])
    }
})
$("#amount2").change(function () {
    st = document.getElementById("amount2").value
    res = st.split(" - ")
    borne1 = res[0]
    borne2 = res[1]
    if (parseInt(borne1, 10) > parseInt(borne2, 10)) {
        alert('first value cant  be bigger then the second value')
    } else {

        $("#slider-range2").slider("values", 0, res[0])
        $("#slider-range2").slider("values", 1, res[1])
    }

});
$('#room_matrix_select_id').on('change', function () {
    $(location).attr('href', ('/matrix/final/' + $('#cont_id').val() + '/' + $("#room_matrix_select_id").val()))
})

function get_spo(id_spo) {
    var data = []
    var id = $(id_spo).find(":selected").attr('value')
    var s = 'http://' + window.location.hostname + '/get_spo/' + id
    if (id !== 0) {
        data = $.ajax({
            type: "GET", //rest Type
            dataType: 'jsonp', //mispelled
            url: s,
            async: false,

            success: function (msg) {
                console.log(this.responseText);
            }
        }).responseText
        data = JSON.parse(data)
    }
    if (id !== 0) {
        if (data[0].checkin === true) {
            $(id_spo).parent().parent().find('#period_checkin_create').show()
            $(id_spo).parent().parent().find('#checkin_from_create').attr('required', true)
            $(id_spo).parent().parent().find('#checkin_to_create').attr('required', true)
        } else {
            $(id_spo).parent().parent().find('#period_checkin_create').hide()
            $(id_spo).parent().parent().find('#checkin_from_create').attr('required', false)
            $(id_spo).parent().parent().find('#checkin_to_create').attr('required', false)
        }
        if (data[0].checkout === true) {
            $(id_spo).parent().parent().find('#period_checkout_create').show()
            $(id_spo).parent().parent().find('#checkout_from_create').attr('required', true)
            $(id_spo).parent().parent().find('#checkout_to_create').attr('required', true)
        } else {
            $(id_spo).parent().parent().find('#period_checkout_create').hide()
            $(id_spo).parent().parent().find('#checkout_from_create').attr('required', false)
            $(id_spo).parent().parent().find('#checkout_to_create').attr('required', false)
        }
        if (data[0].date_creation === true) {
            $(id_spo).parent().parent().find('#period_creation_create').show()
            $(id_spo).parent().parent().find('#creation_from_create').attr('required', true)
            $(id_spo).parent().parent().find('#creation_to_create').attr('required', true)
        } else {
            $(id_spo).parent().parent().find('#period_creation_create').hide()
            $(id_spo).parent().parent().find('#creation_from_create').attr('required', false)
            $(id_spo).parent().parent().find('#creation_to_create').attr('required', false)
        }
        if (data[0].age === true) {
            $(id_spo).parent().parent().find('#age_create').show()
            $(id_spo).parent().parent().find('#age_from_create').attr('required', true)
            $(id_spo).parent().parent().find('#age_to_create').attr('required', true)
        } else {
            $(id_spo).parent().parent().find('#age_create').hide()
            $(id_spo).parent().parent().find('#age_from_create').attr('required', false)
            $(id_spo).parent().parent().find('#age_to_create').attr('required', false)
        }
        if (data[0].night_number === true) {
            $(id_spo).parent().parent().find('#night_number_create').show()
            $(id_spo).parent().parent().find('#night_number_from_create').attr('required', true)
            $(id_spo).parent().parent().find('#night_number_to_create').attr('required', true)
        } else {
            $(id_spo).parent().parent().find('#night_number_create').hide()
            $(id_spo).parent().parent().find('#night_number_from_create').attr('required', false)
            $(id_spo).parent().parent().find('#night_number_to_create').attr('required', false)
        }
        if (data[0].date_stay === true) {
            $(id_spo).parent().parent().find('#period_stay_create').show()
            $(id_spo).parent().parent().find('#stay_from_create').attr('required', true)
            $(id_spo).parent().parent().find('#stay_to_create').attr('required', true)
        } else {
            $(id_spo).parent().parent().find('#period_stay_create').hide()
            $(id_spo).parent().parent().find('#stay_from_create').attr('required', false)
            $(id_spo).parent().parent().find('#stay_to_create').attr('required', false)
        }
        if (data[0].pay_stay === true) {

        }
    } else {
        $(id_spo).parent().parent().find('#period_checkin_create').hide()
        $(id_spo).parent().parent().find('#checkin_from_create').attr('required', false)
        $(id_spo).parent().parent().find('#checkin_to_create').attr('required', false)
        $(id_spo).parent().parent().find('#period_checkout_create').hide()
        $(id_spo).parent().parent().find('#checkout_from_create').attr('required', false)
        $(id_spo).parent().parent().find('#checkout_to_create').attr('required', false)
        $(id_spo).parent().parent().find('#period_creation_create').hide()
        $(id_spo).parent().parent().find('#creation_from_create').attr('required', false)
        $(id_spo).parent().parent().find('#creation_to_create').attr('required', false)
    }
}

$('.single_content_spo').mouseenter(function () {
    $(this).parent().find('#spo_buttons').fadeIn(0);
}).mouseleave(function () {
    $(this).parent().find('#spo_buttons').fadeOut(0);
})
$('.big_content_div').parent().mouseenter(function () {
    $(this).parent().find('.meal_title_div').show(0);
}).parent().mouseleave(function () {
    $(this).parent().find('.meal_title_div').hide(0);
})

function get_spo_room(id_room, id_edit) {
    var data = [];

    var url1 = 'http://' + window.location.hostname + '/get_spo_edit/' + id_room + '?id_edit=' + id_edit;
    data = $.ajax({
        type: "GET", //rest Type
        dataType: 'jsonp', //mispelled
        url: url1,
        async: false,

        success: function (msg) {
            console.log(this.responseText);
        }
    }).responseText;
    data = JSON.parse(data);
    var the_correct_modal = $('#aaaa' + id_edit)
    var the_correct_div = the_correct_modal.find('#non_commulable')
    the_correct_div.empty()
    for (i = 0; i < data.length; i++) {

        if (data[i].allready_chosen == true) {
            the_correct_div.append("<li data-toggle='tooltip' data-placement='top' title='" + data[i].tooltip + "'  class='list-group-item' style='display: flex;'> <label class='custom-control material-checkbox'><input type='checkbox' checked='true'  id='spo_commutable" + data[i].id + "' value='" + data[i].ids + "'name='spo_commutable" + data[i].id + "'class='material-control-input'  > <span class='material-control-description'>" + data[i].name + "</span><span class='material-control-indicator'></span></label></li>"
            )
        } else {
            the_correct_div.append("<li data-toggle='tooltip' data-placement='top' title='" + data[i].tooltip + "' class='list-group-item' style='display: flex;'> <label class='custom-control material-checkbox'><input type='checkbox'  id='spo_commutable" + data[i].id + "' value='" + data[i].ids + "'name='spo_commutable" + data[i].id + "'class='material-control-input'  > <span class='material-control-description'>" + data[i].name + "</span><span class='material-control-indicator'></span></label></li>"
            )
        }


    }

}

function copy_mass(id_content, data, mdl_name, id_h) {
    $('.toast').toast('show', {
        'delay': 5000,
        'autohide': false
    })
    $("[value=" + id_content + "]")['0'].style.display = 'none';
    $('.buttons_wrapper1').append('<button id="paste_button1" type="button"\n' +
        '                   value="' + id_content + '"                                         ' +
        ' class="btn btn-light"\n' +
        'data-toggle="tooltip" data-placement="top" title="' + data + '"' +
        '                                                                                onclick="coller_mass(' + id_content + ',this)"\n' +
        '                                                                        >\n' +
        '                                                                            <i class="fas fa-paste"></i>\n' +
        '                                                                        </button>');
    for (var iter = 2; iter < $("[id=" + id_h + "]")['0'].children[1].children.length; iter++) {

        $("[id=" + id_h + "]")['0'].children[1].children[iter].style.display = 'none';
    }
}

function coller_mass(inte, b) {
    $('#' + inte).clone().appendTo(b.parentNode.parentNode.firstElementChild.children[1])
    var data = [];
    var id_copier = inte;
    var y = b.parentNode.parentNode.getAttribute("id")
    var model_name_p = $('#' + b.parentNode.parentNode.getAttribute("id")).find('#model_name')[0].value
    var model_name_c = $('#' + inte).parent().parent().find('#model_name').val()
    data = $.ajax({
        type: "GET", //rest Type
        dataType: 'jsonp', //mispelled
        url: 'http://' + window.location.hostname + '/matrix/copy_price_masse?id_copy=' + inte + '&id_paste=' + y
            + '&model_name_paste=' + model_name_p + '&model_name_copy=' + model_name_c,
        async: false,

        success: function (msg) {
            console.log(this.responseText);
        }
    }).responseText;

}