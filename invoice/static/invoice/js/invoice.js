$(document).ready(function() {
    if ($('#id_is_paid').is(":checked")) {

        $('input').each(
            function (index) {
                let input = $(this);
                input.prop('readonly', true);
                //input.prop("readonly",true);
            });

        $('#id_related_invoice_item-ADD').hide();
        $('option:not(:selected)').remove();
        $('.footer').hide();
        $('#id_is_final').prop('disabled', true).prop('name', '');
        let elem = $('div').find('[data-contentpath="is_final"]');
        elem.append('<input id="id_is_final" type="hidden" name="is_final" value="true">');

        $('#id_datetime').prop('disabled', true).prop('name', '');
        let elem_datetime = $('div').find('[data-contentpath="datetime"]');
        let datetime_value = elem_datetime.find('#id_datetime').val();
        elem_datetime.append('<input id="id_datetime" type="hidden" name="datetime" value="' + datetime_value + '">');


        //console.log($('div').find('[data-contentpath="is_final"]'));
        if ($('#id_is_paid').is(":checked")) {
            $('#id_is_paid').prop('disabled', true).prop('name', '');
            $('div').find('[data-contentpath="is_final"]').append('<input id="id_is_cancel" type="hidden" name="is_cancel" value="true">')
        }
    }

    //$('input[name="csrfmiddlewaretoken"]').prop('readonly', false);

});