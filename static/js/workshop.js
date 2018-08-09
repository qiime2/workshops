// Dynamic Admin forms
$(document).ready(function() {
    var rateSetButton = $('#rate_set-group .add-row');
    var discount_set = $('[id^=id_rate_set-][id$=-private]');
    var discount_code_set = $('[id^=id_rate_set-][id$=-discount_code]');

    // More rates were added, add them to the discount rate set
    function docChanged() {
        discount_set = $('[id^=id_rate_set-][id$=-private]');
        for (var i = 0; i < discount_set.length; i++){
            var id = discount_set[i].id.split('-').slice(0, 2).join('-');
            $('#' + id +'-discount_code').attr('placeholder', 'Optional - will auto-populate if left blank');
        }
        discount_set.on('change', onDiscountCheck);
    }

    // A rate was changed, toggle it's code view and URL
    function onDiscountCheck(e) {
      var id = e.target.id.split('-').slice(0, 2).join('-');
        $('#' + id + '-discount_code').toggle($(e.target).is(':checked'));
        if ($(e.target).is(':checked')) {
            $('<div><small>URL: https://workshops.qiime2.org/'+ $('#id_slug').val() +'/?rate=<span id="' + id + '-discount_code_customURL">'+ $('#' + id + '-discount_code').val() +'</span></small></div>').insertAfter('#' + id + '-discount_code');
        } else {
            $('#' + id + '-discount_code').next('div').remove();
        }
    }

    // Handle discount code changing to update live display of link
    function onCodeChange(e) {
        $('#'+ e.target.id + '_customURL').text($(e.target).val())
    }

    // Set change and input listeners
    rateSetButton.on('click', docChanged);
    discount_set.on('change', onDiscountCheck);
    discount_code_set.on('input', onCodeChange);

    // Run functions so screen matches initial conditions
    for (var i = 0; i < discount_set.length; i++){
        var id = discount_set[i].id.split('-').slice(0, 2).join('-');
        $('#' + id + '-discount_code').toggle($(discount_set[i]).is(':checked'));
        $('#' + id + '-discount_code').attr('placeholder', 'Optional - will auto-populate if left blank');
        if ($(discount_set[i]).is(':checked')) {
            $('<div><small>URL: https://workshops.qiime2.org/'+ $('#id_slug').val() +'/?rate=<span id="' + id + '-discount_code_customURL">'+ $('#' + id + '-discount_code').val() +'</span></small></div>').insertAfter('#' + id + '-discount_code');
        }
    }
});
