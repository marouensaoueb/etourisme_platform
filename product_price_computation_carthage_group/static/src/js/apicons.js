var order = 0

function get_hotels() {
    var data = []
    var id = $('#state_selection').find(":selected").attr('value')
    var s = 'http://' + window.location.hostname + '/get_hotels/' + id
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
    console.log(data)
    $('#hotel_selection').empty()
    $('#hotel_selection').append('<option name="hotel_id" id="hotel_id">Choose a Hotel</option>')
    for (i = 0; i < data.length; i++) {

        $('#hotel_selection').append("<option id='hotel_id' value='" + data[i].id + "' name='hotel_id'>" + data[i].hotel_name + "</option>")
    }
}


function change_valeur() {
    var selectedvalue = document.getElementById('inputGroupSelectFilter').value;
    console.log(selectedvalue)

}

function get_accomodations(max, min) {
    var data = [];
    var maximum = max;
    var minimum = min;
    var url1 = 'http://' + window.location.hostname + '/get_accomodations/?max=' + max + '&min=' + min;
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
    $('#collapseOne ul').empty();
    for (i = 0; i < data.length; i++) {
        $('#collapseOne ul').append("<li class='list-group-item' style=\"    display: flex;\">"
            + "<label class='custom-control material-checkbox'>" +
            "<input type='checkbox' id='is_acc_form" + data[i].id + "' value='" + data[i].id + "'name='is_acc_form" + data[i].id + "'class='material-control-input'/>" +
            "<span class='material-control-indicator'></span>" +
            "<span class='material-control-description'></span>" +
            "</label>"
            + data[i].accomodation_name + '</li>'
        )
    }

}

function get_accomodations_room(id_room) {
    var data = [];
    var id = id_room;
    var url1 = 'http://' + window.location.hostname + '/get_accomodations_room/?room=' + id;
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
    $('#collapseOne ul').empty();
    for (i = 0; i < data.length; i++) {
        if (data[i].is_avaible === true) {
            $('#collapseOne ul').append("<li class='list-group-item' style=\"    display: flex;\">"
                + "<label class='custom-control material-checkbox'>" +
                "<input type='checkbox' id='is_acc_form" + data[i].id + "' value='" + data[i].id + "'name='is_acc_form" + data[i].id + "'class='material-control-input' onclick='return false' checked='true'>" +
                "<span class='material-control-indicator'></span>" +
                "<span class='material-control-description'></span>" +
                "</label>"
                + data[i].accomodation_name + '</li>'
            )
        } else {
            $('#collapseOne ul').append("<li class='list-group-item' style=\"    display: flex;\">"
                + "<label class='custom-control material-checkbox'>" +
                "<input type='checkbox' id='is_acc_form" + data[i].id + "' value='" + data[i].id + "'name='is_acc_form" + data[i].id + "'class='material-control-input' onclick='return false'/>" +
                "<span class='material-control-indicator'></span>" +
                "<span class='material-control-description'></span>" +
                "</label>"
                + data[i].accomodation_name + '</li>'
            )

        }
    }

}

function getmeals_room(id_room) {
    var data = [];
    var id = id_room;
    var url1 = 'http://' + window.location.hostname + '/get_meals_room/?room=' + id;
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
    $('#collapseOneOne ul').empty();
    for (i = 0; i < data.length; i++) {
        if (data[i].is_avaible === true) {
            $('#collapseOneOne ul').append("<li class='list-group-item' style=\"    display: flex;\">"
                + "<label class='custom-control material-checkbox'>" +
                "<input type='checkbox' id='is_acc_form" + data[i].id + "' value='" + data[i].id + "'name='is_acc_form" + data[i].id + "'class='material-control-input' onclick='return false' checked ='true'>" +
                "<span class='material-control-indicator'></span>" +
                "<span class='material-control-description'></span>" +
                "</label>"
                + data[i].meal_name + '</li>'
            )
        } else {
            $('#collapseOneOne ul').append("<li class='list-group-item' style=\"    display: flex;\">"
                + "<label class='custom-control material-checkbox'>" +
                "<input type='checkbox' id='is_acc_form" + data[i].id + "' value='" + data[i].id + "'name='is_acc_form" + data[i].id + "'class='material-control-input' onclick='return false'/>" +
                "<span class='material-control-indicator'></span>" +
                "<span class='material-control-description'></span>" +
                "</label>"
                + data[i].meal_name + '</li>'
            )

        }
    }

}

$(document).ready(function () {
    $("#room_min_form").on("keyup", function () {
        // if (!($("#room_max_form").is(':empty'))){
        var m1 = document.getElementById('room_max_form').value
        var m2 = document.getElementById('room_min_form').value
        if (!(m1 === '')) {
            get_accomodations(m1, m2)
        }

        // }


    })
    $("#room_max_form").on("keyup", function () {
        // if (!($("#room_min_form").is(':empty'))){
        var m1 = document.getElementById('room_max_form').value
        var m2 = document.getElementById('room_min_form').value
        if (!(m2 === '')) {
            get_accomodations(m1, m2)
        }        // }


    })

})
$(document).ready(function () {
    var id_room = document.getElementById('room_json_id').value
    get_accomodations_room(id_room)
    getmeals_room(id_room)

})

$(document).ready(function () {

    $("#search_hotel").on("keyup", function () {

        var value = $(this).val().toLowerCase();

        var byfilter = document.querySelector('#inputGroupSelectFilter').value
        if ($("#search_hotel").val().length == 0) {
            $("#accordionExample li").filter(function () {
                // var x = $(this).text().toLowerCase().indexOf(value) > -1
                $(this).toggle($(this).text().toLowerCase().indexOf(value) == -1)

                // if ( $(this).text().toLowerCase().indexOf(value) > -1){
                //     $(this).toggle(  );
                // }
                // $(this).parent().parent().parent().parent().toggle($(this).text().toLowerCase().indexOf(value) > -1)

            });
        } else if (byfilter === "1") {
            $("#accordionExample li").filter(function () {
                // var x = $(this).text().toLowerCase().indexOf(value) > -1
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)

                // if ( $(this).text().toLowerCase().indexOf(value) > -1){
                //     $(this).toggle(  );
                // }
                // $(this).parent().parent().parent().parent().toggle($(this).text().toLowerCase().indexOf(value) > -1)

            });

        } else if (byfilter === "2") {
            $("#accordionExample .card").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        }

    });
});
$('#duplicate_div').click(function () {
    var x = '<div id="formula-div_' + (order + 1) + '"\n' +
        '                                                                 class="form-group formula-div form-inline">\n' +
        '                                                                <div class="input-group ">\n' +
        '                                                                    <div class="input-group-prepend">\n' +
        '                                                                        <span class="input-group-text"\n' +
        '                                                                              id="basic-addon3">meal\n' +
        '                                                                        </span>\n' +
        '                                                                    </div>\n' +
        '\n' +
        '                                                                    <select id="meal_formula" name="meal_formula"\n' +
        '                                                                            class="form-control">\n' +
        '                                                                        <option t-attf-value="all_meals">All meals\n' +
        '                                                                        </option>\n' +
        '                                                                        <t t-foreach="request.env[\'room.meal\'].search([])"\n' +
        '                                                                           t-as="currency">\n' +
        '                                                                            <option t-attf-value="{{currency.id}}">\n' +
        '                                                                                <t t-esc="currency.code"/>\n' +
        '                                                                            </option>\n' +
        '                                                                        </t>\n' +
        '\n' +
        '\n' +
        '                                                                    </select>\n' +
        '                                                                </div>\n' +
        '                                                                <div class="input-group ">\n' +
        '                                                                    <div class="input-group-prepend">\n' +
        '                                                                        <span class="input-group-text"\n' +
        '                                                                              id="basic-addon3">accomodation\n' +
        '                                                                        </span>\n' +
        '                                                                    </div>\n' +
        '\n' +
        '                                                                    <select id="accomodation_formula"\n' +
        '                                                                            name="accomodation_formula"\n' +
        '                                                                            class="form-control">\n' +
        '                                                                        <option t-attf-value="all_accomodations">All\n' +
        '                                                                            accomodations\n' +
        '                                                                        </option>\n' +
        '                                                                        <t t-foreach="request.env[\'accomodations\'].search([])"\n' +
        '                                                                           t-as="currency">\n' +
        '                                                                            <option t-attf-value="{{currency.id}}">\n' +
        '                                                                                <t t-esc="currency.code"/>\n' +
        '                                                                            </option>\n' +
        '                                                                        </t>\n' +
        '\n' +
        '\n' +
        '                                                                    </select>\n' +
        '                                                                </div>\n' +
        '                                                                <div class="input-group ">\n' +
        '                                                                    <div class="input-group-prepend">\n' +
        '                                                                        <span class="input-group-text"\n' +
        '                                                                              id="basic-addon3">operand\n' +
        '                                                                        </span>\n' +
        '                                                                    </div>\n' +
        '\n' +
        '                                                                    <select id="operand_formula" name="operand_formula"\n' +
        '                                                                            class="form-control">\n' +
        '                                                                        <option t-attf-value="+">+</option>\n' +
        '                                                                        <option t-attf-value="*">*</option>\n' +
        '                                                                        <option t-attf-value="/">/</option>\n' +
        '                                                                        <option t-attf-value="-">-</option>\n' +
        '\n' +
        '\n' +
        '                                                                    </select>\n' +
        '                                                                </div>\n' +
        '                                                                <div class="input-group ">\n' +
        '                                                                    <div class="input-group-prepend">\n' +
        '                                                                        <span class="input-group-text"\n' +
        '                                                                              id="basic-addon3">value\n' +
        '                                                                        </span>\n' +
        '                                                                    </div>\n' +
        '\n' +
        '                                                                    <input type="number" id="value_formula"\n' +
        '                                                                           name="value_formula" class="form-control"/>\n' +
        '                                                                </div>\n' +
        '                                                                <div class="input-group ">\n' +
        '                                                                    <div class="input-group-prepend">\n' +
        '                                                                        <span class="input-group-text"\n' +
        '                                                                              id="basic-addon3">order\n' +
        '                                                                        </span>\n' +
        '                                                                    </div>\n' +
        '\n' +
        '                                                                    <input type="number" id="order_formula"\n' +
        '                                                                           name="order_formula"  class="form-control"/>\n' +
        '                                                                </div>\n' +
        '                                                                <button id="confirm_operation" type="button" class="btn"><i class="fa fa-check"></i> </button>\n' +
        '                                                            </div>'
    $('#formula-wrapper').prepend(x)
    order = order + 1
})
$('#confirm_operation').click(function () {
    $(this).parent().css('border-color', 'green');
    $(this).css('color', 'green');
    $(this).parent().find('#order_formula').val(order + 1)
    $(this).parent().attr("id", order + 1);
})

function get_spo_mass(id_spo) {
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
            $(id_spo)[0].parentElement.parentElement.children[2].style.display = 'block'

            $('#checkin_from_create_mass').attr('required', true)
            $('#checkin_to_create_mass').attr('required', true)
        } else {
            $(id_spo)[0].parentElement.parentElement.children[2].style.display = 'none'
            $('#checkout_from_create_mass').attr('required', false)
            $('#checkin_to_create_mass').attr('required', false)
        }
        if (data[0].checkout === true) {
            $(id_spo)[0].parentElement.parentElement.children[3].style.display = 'block'
            $('#checkout_from_create_mass').attr('required', false)
            $('#checkout_to_create_mass').attr('required', false)
        } else {
            $(id_spo)[0].parentElement.parentElement.children[3].style.display = 'none'
            $('#checkin_from_create_mass').attr('required', false)
            $('#checkout_to_create_mass').attr('required', false)
        }
        if (data[0].date_creation === true) {
            $(id_spo)[0].parentElement.parentElement.children[4].style.display = 'block'
            $('#creation_from_create_mass').attr('required', true)
            $('#creation_to_create_mass').attr('required', true)
        } else {
            $(id_spo)[0].parentElement.parentElement.children[4].style.display = 'none'
            $('#creation_from_create_mass').attr('required', false)
            $('#creation_to_create_mass').attr('required', false)
        }
        if (data[0].age === true) {
            $(id_spo)[0].parentElement.parentElement.children[6].style.display = 'block'
            $('#age_min_mass').attr('required', true)
            $('#age_max_mass').attr('required', true)
        } else {
            $(id_spo)[0].parentElement.parentElement.children[6].style.display = 'none'
            $('#age_min_mass').attr('required', false)
            $('#age_max_mass').attr('required', false)
        }
        if (data[0].night_number === true) {
            $(id_spo)[0].parentElement.parentElement.children[7].style.display = 'block'
            $('#number_min_form').attr('required', true)
            $('#number_max_form').attr('required', true)
        } else {
            $(id_spo)[0].parentElement.parentElement.children[7].style.display = 'none'
            $('#number_min_form').attr('required', false)
            $('#number_max_form').attr('required', false)
        }
        if (data[0].date_stay === true) {
            $(id_spo)[0].parentElement.parentElement.children[5].style.display = 'block'
            $('#stay_from_create_mass').attr('required', true)
            $('#stay_to_create_mass').attr('required', true)
        } else {
            $(id_spo)[0].parentElement.parentElement.children[5].style.display = 'none'
            $('#stay_from_create_mass').attr('required', false)
            $('#stay_to_create_mass').attr('required', false)
        }
        if (data[0].pay_stay === true) {

        }
    } else {
        $(id_spo)[0].parentElement.parentElement.children[2].style.display = 'none'
        $('#checkin_from_create_mass').attr('required', false)
        $('#checkin_to_create_mass').attr('required', false)
        $(id_spo)[0].parentElement.parentElement.children[3].style.display = 'none'
        $('#checkin_from_create_mass').attr('required', false)
        $('#checkout_to_create_mass').attr('required', false)
        $(id_spo)[0].parentElement.parentElement.children[4].style.display = 'none'
        $('#creation_from_create_mass').attr('required', false)
        $('#creation_to_create_mass').attr('required', false)
        $(id_spo)[0].parentElement.parentElement.children[5].style.display = 'none'
        $('#stay_from_create_mass').attr('required', false)
        $('#stay_to_create_mass').attr('required', false)
        $(id_spo)[0].parentElement.parentElement.children[6].style.display = 'none'
        $('#age_min_mass').attr('required', false)
        $('#age_max_mass').attr('required', false)
        $(id_spo)[0].parentElement.parentElement.children[7].style.display = 'none'
        $('#number_min_form').attr('required', false)
        $('#number_max_form').attr('required', false)
    }
}
function check_all(source) {

      for(var j=1;j<4;j++){
        for (var k=0;k<source.parentElement.parentElement.parentElement.parentElement.children[j].children.length;k++){
            source.parentElement.parentElement.parentElement.parentElement.children[j].children[k].children[0].children[0].children[0].children[0].checked=source.checked;
        };
      };


}