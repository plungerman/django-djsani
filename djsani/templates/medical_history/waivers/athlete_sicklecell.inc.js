<script type="text/javascript" charset="utf-8">
$(function() {
    /* if waive, uncheck proof & vice-versa */
    $('#waive').on('change', function() {
        $('input').not(this).prop('checked', false);
    });
    $('#proof').on('change', function() {
        $('input').not(this).prop('checked', false);
    });
    /* if the user goes straight for the radios */
    $('input[name="results"]').change(
        function(){
            $('#proof').prop('checked', true);
            $('#waive').prop('checked', false);
        }
    );
    /* verify the form before going to server */
    $('#sickle_cell').submit(function() {
        if ($('input:checkbox', this).is(':checked')) {
            if ($('#proof').is(':checked')) {
                if ($('input:radio', this).is(':checked')) {
                    // disable submit
                    $(this).children('input[type=submit]').attr('disabled', 'disabled');
                    return true;
                } else {
                    alert('You must indicate "Positive or Negative" results');
                    return false;
                }
            } else {
                // disable submit
                $(this).children('input[type=submit]').attr('disabled', 'disabled');
                return true;
            }
        } else {
            alert('You must choose to waive or provide proof.');
            return false;
        }
    });
});
</script>
