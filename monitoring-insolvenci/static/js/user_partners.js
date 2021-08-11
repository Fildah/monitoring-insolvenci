function format(data) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<td>' +
        '<td class="align-top">' +
        '<div class="card-deck">' +
        '<div class="card">' +
        '<div class="card-body border border-primary">' +
        '<h5 class="card-title">Adresa sídla</h5>' +
        '<ul class="list-group list-group-flush">' +
        '<li class="list-group-item">' + data.street_address + '</li>' +
        '<li class="list-group-item">' + data.city_part + '</li>' +
        '<li class="list-group-item">' + data.city + '</li>' +
        '<li class="list-group-item">' + data.zip_code + '</li>' +
        '<li class="list-group-item">' + data.country + '</li>' +
        '</ul>' +
        '</div>' +
        '</div>' +
        '</td>' +
        '<td class="align-top">' +
        '<div class="card">' +
        '<div class="card-body border border-primary">' +
        '<h5 class="card-title">Obecné informace</h5>' +
        '<ul class="list-group list-group-flush">' +
        '<li class="list-group-item">Založeno: ' + data.business_start + '</li>' +
        '<li class="list-group-item">Ukončeno: ' + data.business_end + '</li>' +
        '<li class="list-group-item">Stav podnikání: ' + data.state + '</li>' +
        '<li class="list-group-item">Právní forma: ' + data.business_form + '</li>' +
        '</ul>' +
        '</div>' +
        '</div>' +
        '</td>' +
        '<td class="align-top">' +
        '<div class="card">' +
        '<div class="card-body border border-danger">' +
        '<h5 class="card-title">Insolvence partnera</h5>' +
        '<ul class="list-group list-group-flush">' +
        '<li class="list-group-item">Celkový počet: ' + data.insolvency_count + '</li>' +
        '<li class="list-group-item">Poslední započatá insolvence: ' + data.insolvency_last_start + '</li>' +
        '<li class="list-group-item">Poslední ukončená insolvence: ' + data.insolvency_last_end + '</li>' +
        '<li class="list-group-item">Poslední stav insolvence: ' + data.insolvency_last_state + '</li>' +
        '</ul>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '</td>' +
        '</tr>' +
        '</table>';
}