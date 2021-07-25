function format(d) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td class="align-top">' +
        '<div class="card" style="width: 18rem;">' +
        '<div class="card-body">' +
        '<h5 class="card-title">Adresa sídla</h5>' +
        '<ul class="list-group list-group-flush">' +
        '<li class="list-group-item">' + d.street + ' ' + d.street_number + '/' + d.orientation_number + '</li>' +
        '<li class="list-group-item">' + d.city_part + '</li>' +
        '<li class="list-group-item">' + d.city + '</li>' +
        '<li class="list-group-item">' + d.zip_code + '</li>' +
        '<li class="list-group-item">' + d.country + '</li>' +
        '</ul>' +
        '</div>' +
        '</div>' +
        '</td>' +
        '<td class="align-top">' +
        '<div class="card" style="width: 18rem;">' +
        '<div class="card-body">' +
        '<h5 class="card-title">Obecné informace</h5>' +
        '<ul class="list-group list-group-flush">' +
        '<li class="list-group-item">Založeno: ' + d.business_started + '</li>' +
        '<li class="list-group-item">Stav podnikání: ' + d.state + '</li>' +
        '<li class="list-group-item">Právní forma: ' + d.business_form + '</li>' +
        '</ul>' +
        '</div>' +
        '</div>' +
        '</tr>' +
        '</table>';
}