$(document).ready(function() {
    $('#id_is_arrived').prop('disabled', true);
    /*
    $('#id_is_done').change(function() {
        if(this.checked) {
            var returnVal = confirm("Are you sure?");
            $(this).prop("checked", returnVal);
            $('#id_is_arrived').prop("checked", "checked");
        }
        $('#textbox1').val(this.checked);        
    });
    */
    if ($('#id_is_done').is(":checked")) {

        $('input').each(
            function (index) {
                let input = $(this);
                input.prop('readonly', true);
                //input.prop("readonly",true);
            });

        $('option:not(:selected)').remove();
        $('#id_date').prop('disabled', true).prop('name', '');
        $('#id_start').prop('disabled', true).prop('name', '');
        let elem = $('div').find('[data-contentpath="is_final"]');
        elem.append('<input id="id_is_final" type="hidden" name="is_final" value="true">');

        $('.footer').hide();

        $('#id_datetime').prop('disabled', true).prop('name', '');
        let elem_datetime = $('div').find('[data-contentpath="datetime"]');
        let datetime_value = elem_datetime.find('#id_datetime').val();
        elem_datetime.append('<input id="id_datetime" type="hidden" name="datetime" value="' + datetime_value + '">');


        //console.log($('div').find('[data-contentpath="is_final"]'));
        if ($('#id_is_done').is(":checked")) {
            $('#id_is_done').prop('disabled', true).prop('name', '');
            $('div').find('[data-contentpath="is_final"]').append('<input id="id_is_cancel" type="hidden" name="is_cancel" value="true">')
        }
    }

    //$('input[name="csrfmiddlewaretoken"]').prop('readonly', false);

});
