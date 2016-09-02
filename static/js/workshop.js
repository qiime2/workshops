// My dislike of jQuery is overshadowed by the ease of this use-case
$(document).ready(function() {
    var publicWorkshop = $('#id_public');
    var privateCodeRow = $('.field-private_code');
    var privateCodeInput = $('#id_private_code');
    var privateCodeUrlSpan = $('#pcode');

    function onInputChange() {
        privateCodeUrlSpan.text(privateCodeInput.val());
    }

    function onPublicCheck() {
        privateCodeRow.toggle(!publicWorkshop.is(':checked'));
    }

    publicWorkshop.on('change', onPublicCheck);
    privateCodeInput.on('input', onInputChange);
    onInputChange();
    onPublicCheck();
});
