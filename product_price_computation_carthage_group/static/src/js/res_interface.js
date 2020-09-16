$('.add_client_button').click(function () {
    gen = $('#clients_detail').find('#gen').val()
    namo = $('#clients_detail').find('#name').val()
    sname = $('#clients_detail').find('#sname').val()
    birth = $('#clients_detail').find('#birth').val()
    age = $('#clients_detail').find('#age').val()
    p_number = $('#clients_detail').find('#p_number').val()
    line = "<tr><td>" + gen + "</td><td>" + namo + "</td><td>" + sname + "</td><td>" + birth + "</td><td>" + age + "</td><td>" + p_number + "</td><td> </td></tr>"
    $('#clients_table').append(line);
});
$('.delete_r').click(function () {
    $('#clients_detail').find('tbody').remove()
})
$('#creation_reservation').click(function () {
        data = []
        var list_client1 = []
        var list_client = []
        for (var iter = 1; iter < document.getElementById("clients_table").rows.length; iter++) {
            var list_client1 = [{
                gender: document.getElementById("clients_table").rows[iter].cells[0].innerHTML,
                name: document.getElementById("clients_table").rows[iter].cells[1].innerHTML,
                surname: document.getElementById("clients_table").rows[iter].cells[2].innerHTML,
                birthday: document.getElementById("clients_table").rows[iter].cells[3].innerHTML,
                age: document.getElementById("clients_table").rows[iter].cells[4].innerHTML,
                passeport_number: document.getElementById("clients_table").rows[iter].cells[5].innerHTML
            }]
            list_client = list_client.concat(list_client1)

        }
        console.log(list_client)
        var reservation = {
            company: document.getElementById("company_id").value,
            hotel: document.getElementById("hotel_id").value,
            tour_operator: document.getElementById("to_id").value,
            tour_operator_ref: document.getElementById("res_to_ref").value,
            currency_id: document.getElementById("currency_id").value,
            reservation_number: null,
            checkin: document.getElementById("check_in").value,
            checkout: document.getElementById("check_out").value,
            creation_date: null,
            sending_date: null,
            meal: document.getElementById("meal").value,
            accomodation: document.getElementById("acc").value,
            room_category: document.getElementById("room_c").value,
            note: document.getElementById("note").value,
            night_number: document.getElementById("night_number").value,
            list_clients: list_client
        }
        reservation = JSON.stringify(reservation)
        var csrf_token = document.getElementById("csrf_token").value
        var postobject = {
            'csrf_token': csrf_token,
            'reservation': reservation
        }
        var s = 'http://' + window.location.hostname + '/reservations/creation/'
        $.post(s, postobject)
            .done(function () {
                window.location.replace('/reservations')
            }).fail(function () {
            alert('error')
        })

    }
)

$('#pager_offset').click(function () {
    $('#pager_offset').toggle()
    $('#pager_offset_edit').toggle()
})
$('#offset').change(function () {

    $('#pager_offset').toggle()
    $('#pager_offset_edit').toggle()
    st = $('#offset').val()
    st = st.replace(/\s/g, '');
    st = st.split("-")
    st = JSON.stringify(st)
    var url = new URL(window.location.href);
    url.searchParams.set('ppg', st)

    window.location.replace(url.href)
})
$('#birth').change(function () {
    var today = new Date();
    var birth = new Date($('#birth').val().replace(/-/g,'/'))
    var diff = Math.abs(today - birth );
    var one_year=(1000*60*60*24) * 365;

    $('#age').val(Math.trunc(diff/one_year))
})
$('#check_out').change(function () {

    var d1 = new Date($('#check_in').val().replace(/-/g,'/'))
    var d2 = new Date($('#check_out').val().replace(/-/g,'/'))
    var diff = Math.abs(d1 - d2  );
    var one_day=1000*60*60*24;

    $('#night_number').val(Math.trunc(diff/one_day))
})
$('#search_button_reset').click(function () {
    window.location.replace('/reservations')
})
$('#search_button').click(function () {
    var search_area = $('#search_parameters')
    var country = search_area.find('#country').val()
    var city = search_area.find('#city').val()
    var to_id = search_area.find('#to_id').val()
    var hotel_id = search_area.find('#hotel_id').val()
    var check_in_f = search_area.find('#check_in_f').val()
    var check_in_t = search_area.find('#check_in_t').val()
    var check_out_f = search_area.find('#check_out_f').val()
    var check_out_t = search_area.find('#check_out_t').val()
    var meal = search_area.find('#meal').val()
    var room_categ = search_area.find('#room_categ').val()
    var accomodation = search_area.find('#accomodation').val()
    var reservation_number = search_area.find('#reservation_number').val()
    var res_to_ref = search_area.find('#res_to_ref').val()
    var note = search_area.find('#note').val()
    st =
        {"country":country,
        "city":city,
        "to_id":to_id,
        "hotel_id":hotel_id,
        "check_in_f":check_in_f,
        "check_in_t":check_in_t,
        "check_out_f":check_out_f,
        "check_out_t":check_out_t,
        "meal":meal,
        "room_categ":room_categ,
        "accomodation":accomodation,
        "reservation_number":reservation_number,
        "note":note,
        "res_to_ref":res_to_ref}

    var s = window.location.origin + '/reservations'
    s = s + '?search=' + JSON.stringify(st)
    window.location.replace(s)
})

function get_hotel_company() {
    var data = [];
    var id_company = $('#company_id').find(":selected").attr('value')
    var url1 = window.location.origin + '/get_hotel_company';
    url1 = url1 + '?id=' + id_company
    if (id_company === "0") {
        $('#hotel_id').empty()
        $('#hotel_id').append("<option value=\"0\">\n" +
            "                                                            select hotel\n" +
            "                                                        </option>")
        $('#room_c').empty()
        $('#room_c').append("<option value=\"0\">\n" +
            "                                                            select room category\n" +
            "                                                        </option>")
        $('#acc').empty()
        $('#acc').append("<option value=\"0\">\n" +
            "                                                            select accomodation\n" +
            "                                                        </option>")
        $('#meal').empty()
        $('#meal').append("<option value=\"0\">\n" +
            "                                                            select meal\n" +
            "                                                        </option>")
    } else {
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
        console.log(data)
        $('#hotel_id').empty()
        $('#hotel_id').append("<option value=\"0\">\n" +
            "                                                            select hotel\n" +
            "                                                        </option>")

        for (i = 0; i < data.length; i++) {
            $('#hotel_id').append("<option id='hotel_id' value='" + data[i].hotel_id + "' name='hotel_id'>" + data[i].hotel_name + "</option>")
        }
    }
}

function get_room_category() {
    var data = [];
    var id_company = $('#company_id').find(":selected").attr('value')
    var id_hotel = $('#hotel_id').find(":selected").attr('value')
    var url1 = window.location.origin + '/get_room_hotel';
    url1 = url1 + '?id_company=' + id_company + '&id_hotel=' + id_hotel
    if (id_hotel === "0") {
        $('#room_c').empty()
        $('#room_c').append("<option value=\"0\">\n" +
            "                                                            select room category\n" +
            "                                                        </option>")
        $('#acc').empty()
        $('#acc').append("<option value=\"0\">\n" +
            "                                                            select accomodation\n" +
            "                                                        </option>")
        $('#meal').empty()
        $('#meal').append("<option value=\"0\">\n" +
            "                                                            select meal\n" +
            "                                                        </option>")
    } else {
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
        console.log(data)
        $('#room_c').empty()
        $('#room_c').append("<option value=\"0\">\n" +
            "                                                            select room category\n" +
            "                                                        </option>")

        for (i = 0; i < data.length; i++) {
            $('#room_c').append("<option id='room_id' value='" + data[i].room_id + "' name='room_id'>" + data[i].room_name + "</option>")
        }
    }
}

function get_meal_acc() {
    var data = [];
    var id_company = $('#company_id').find(":selected").attr('value')
    var id_hotel = $('#hotel_id').find(":selected").attr('value')
    var id_room = $('#room_c').find(":selected").attr('value')

    var url1 = window.location.origin + '/get_meal_accomodation';
    url1 = url1 + '?company_id=' + id_company + '&hotel_id=' + id_hotel + '&room_id=' + id_room
    if (id_room === "0") {
        $('#acc').empty()
        $('#acc').append("<option value=\"0\">\n" +
            "                                                            select accomodation\n" +
            "                                                        </option>")
        $('#meal').empty()
        $('#meal').append("<option value=\"0\">\n" +
            "                                                            select meal\n" +
            "                                                        </option>")
    } else {
        data = $.ajax({
            type: "GET", //rest Type
            dataType: 'jsonp', //mispelled
            url: url1,
            async: false,

            success: function (msg) {
                console.log(this.responseText);
            }
        }).responseText;
        console.log(data)

        data = JSON.parse(data);
        console.log(data)
        $('#acc').empty()
        $('#acc').append("<option value=\"0\">\n" +
            "                                                            select accomodation\n" +
            "                                                        </option>")
        $('#meal').empty()
        $('#meal').append("<option value=\"0\">\n" +
            "                                                            select meal\n" +
            "                                                        </option>")

        for (i = 0; i < data.list_meal.length; i++) {
            $('#meal').append("<option id='meal' value='" + data.list_meal[i].meal_id + "' name='meal'>" + data.list_meal[i].meal_name + "</option>")
        }
        for (i = 0; i < data.list_acc.length; i++) {
            $('#acc').append("<option id='acc' value='" + data.list_acc[i].acc_id + "' name='room_id'>" + data.list_acc[i].acc_name + "</option>")
        }
    }
}

$('#order_reservation_select').change(function () {
    var url = new URL(window.location.href);

    if (this.value === '0') {
        $('#order_reservation_sense').hide()
        url.searchParams.set('order', this.value)
        url.searchParams.delete('sense')
        window.location.replace(url.href)

    } else {
        $('#order_reservation_sense').show()
        url.searchParams.set('order', this.value)
        url.searchParams.set('sense', '0')
        window.location.replace(url.href)



    }

})
$('#order_reservation_sense').change(function () {
    var url1 = new URL(window.location.href);
    url1.searchParams.set('sense', this.value)
    window.location.replace(url1.href)
})