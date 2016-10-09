// Dynamic Admin forms
$(document).ready(function() {
    var publicWorkshop = $('#id_public');
    var privateCodeRow = $('.field-private_code');
    var privateCodeInput = $('#id_private_code');
    var privateCodeUrlSpan = $('#pcode');
    var rateSetButton = $('#rate_set-group .add-row');
    var discount_set = $('[id^=id_rate_set-][id$=-discount]');
    var discount_code_set = $('[id^=id_rate_set-][id$=-discount_code]');

    function onInputChange() {
        privateCodeUrlSpan.text(privateCodeInput.val());
    }

    function onPublicCheck() {
        privateCodeRow.toggle(!publicWorkshop.is(':checked'));
    }

    function docChanged() {
        discount_set = $('[id^=id_rate_set-][id$=-discount]');
        for (var i = 0; i < discount_set.length; i++){
            $('#' + discount_set[i].id +'_code').attr('placeholder', 'Optional - will auto-populate if left blank');
        }
        discount_set.on('change', onDiscountCheck);
    }

    function onDiscountCheck(e) {
        $('#' + e.target.id + '_code').toggle($(e.target).is(':checked'));
        if ($(e.target).is(':checked')) {
            $('<div><small>URL: https://workshops.qiime.org/'+ $('#id_slug').val() +'/?rate=<span id="' + e.target.id + '_code_customURL">'+ $('#' + e.target.id + '_code').val() +'</span></small></div>').insertAfter('#' + e.target.id + '_code')
        } else {
            $('#' + e.target.id + '_code').next('div').remove();
        }
    }

    function onCodeChange(e) {
        $('#'+ e.target.id + '_customURL').text($(e.target).val())
    }

    // Set listeners
    publicWorkshop.on('change', onPublicCheck);
    rateSetButton.on('click', docChanged);
    privateCodeInput.on('input', onInputChange);
    discount_set.on('change', onDiscountCheck);
    discount_code_set.on('input', onCodeChange);

    // Run functions so screen matches initial conditions
    onInputChange();
    onPublicCheck();
    for (var i = 0; i < discount_set.length; i++){
        $('#' + discount_set[i].id + '_code').toggle($(discount_set[i]).is(':checked'));
        $('#' + discount_set[i].id +'_code').attr('placeholder', 'Optional - will auto-populate if left blank');
        if ($(discount_set[i]).is(':checked')) {
            $('<div><small>URL: https://workshops.qiime.org/'+ $('#id_slug').val() +'/?rate=<span id="' + discount_set[i].id + '_code_customURL">'+ $('#' + discount_set[i].id + '_code').val() +'</span></small></div>').insertAfter('#' + discount_set[i].id + '_code')
        }
    }
});
