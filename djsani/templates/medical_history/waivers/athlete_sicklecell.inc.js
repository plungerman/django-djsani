<script type="text/javascript" charset="utf-8">
$(function() {
  var dict = {};
  dict.sickleCell1 = false;
  dict.sickleCell2 = false;

  $('.modal-video').magnificPopup({
    disableOn: 700,
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: false,
    fixedContentPos: false
  });
  $('.modal-video').click(function(){
    $dis = $(this).attr('id');
    dict[$dis] = true;
    console.log($dis);
    if (dict.sickleCell1 == true && dict.sickleCell2 == true) {
      $('#id_submit').prop('disabled', false);
      console.log('done');
    }
  });
  $('#id_submit').prop('disabled', true);

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
          $('#id_submit').prop('disabled', true);
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
