function format(data) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td class="align-top">' +
        '<div class="card" style="width: 18rem;">' +
        '<div class="card-body">' +
        '<h5 class="card-title">Adresa sídla</h5>' +
        '<ul class="list-group list-group-flush">' +
        '<li class="list-group-item">' + data.street + ' ' + data.street_number + '/' + data.orientation_number + '</li>' +
        '<li class="list-group-item">' + data.city_part + '</li>' +
        '<li class="list-group-item">' + data.city + '</li>' +
        '<li class="list-group-item">' + data.zip_code + '</li>' +
        '<li class="list-group-item">' + data.country + '</li>' +
        '</ul>' +
        '</div>' +
        '</div>' +
        '</td>' +
        '<td class="align-top">' +
        '<div class="card" style="width: 18rem;">' +
        '<div class="card-body">' +
        '<h5 class="card-title">Obecné informace</h5>' +
        '<ul class="list-group list-group-flush">' +
        '<li class="list-group-item">Datum vzniku: ' + data.business_start + '</li>' +
        '<li class="list-group-item">Datum zániku: ' + data.business_end + '</li>' +
        '<li class="list-group-item">Stav podnikání: ' + data.state + '</li>' +
        '<li class="list-group-item">Právní forma: ' + data.business_form + '</li>' +
        '</ul>' +
        '</div>' +
        '</div>' +
        '</tr>' +
        '</table>';
}