// My dislike of jQuery is overshadowed by the ease of this use-case
$(document).ready(function() {
    var publicWorkshop = $('#id_public');
    var privateCodeRow = $('.field-private_code');
    var privateCodeInput = $('#id_private_code');
    var privateCodeUrlSpan = $('#pcode');
    var rateSetButton = $('#rate_set-group .add-row');
    var discount_set = $('[id^=id_rate_set-][id$=-discount]');

    function onInputChange() {
        privateCodeUrlSpan.text(privateCodeInput.val());
    }

    function onPublicCheck() {
        privateCodeRow.toggle(!publicWorkshop.is(':checked'));
    }

    function docChanged() {
        discount_set = $('[id^=id_rate_set-][id$=-discount]');
        discount_set.on('change', onDiscountCheck);
    }

    function onDiscountCheck(e) {
        $('#' + e.target.id + '_code').toggle($(e.target).is(':checked'));
    }

    publicWorkshop.on('change', onPublicCheck);
    rateSetButton.on('click', docChanged);
    privateCodeInput.on('input', onInputChange);
    discount_set.on('change', onDiscountCheck);
    onInputChange();
    onPublicCheck();
    for (var i = 0; i < discount_set.length; i++){
        $('#' + discount_set[i].id + '_code').toggle($(discount_set[i]).is(':checked'));
    }
});
