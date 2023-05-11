$(function() {
  $("body").toggleClass("sidenav-toggled");
  /* spinner */
  var opts = {
      lines: 13, // The number of lines to draw
      length: 20, // The length of each line
      width: 10, // The line thickness
      radius: 30, // The radius of the inner circle
      corners: 1, // Corner roundness (0..1)
      rotate: 0, // The rotation offset
      direction: 1, // 1: clockwise, -1: counterclockwise
      color: '#000', // #rgb or #rrggbb or array of colors
      speed: 1, // Rounds per second
      trail: 60, // Afterglow percentage
      shadow: false, // Whether to render a shadow
      hwaccel: false, // Whether to use hardware acceleration
      className: 'search-results', // The CSS class to assign to spinner
      zIndex: 2e9, // The z-index (defaults to 2000000000)
      top: '50px', // Top position relative to parent in px
      left: 'auto' // Left position relative to parent in px
  };
  var target = document.getElementById("students-data-panel");
  var spinner = new Spinner(opts).spin(target);
  spinner.stop(target);

  /*  Initialise the DataTables:
      we assign it to variable 'table' so that we can use it for
      the 'on change' event handler below. if we do not do it this
      way, then the 'on change' event does not work for items after
      page 1 or for items returned by search.
  */

  var table = $('#students-data').DataTable({
      buttons: [
        {
            text: 'CSV',
            extend: 'csv',
            fieldSeparator: '|',
            extension: '.csv'
        },
        'excel'
      ],
      dom: 'lfrBtip',
      order: [[4, "asc"]],
      lengthMenu: [
          [100, 250, 500, 1000, 2000, -1],
          [100, 250, 500, 1000, 2000, "All"]
      ],
      drawCallback: function() {
          $('[data-toggle="popover"]').popover({
              trigger: 'hover',
              'placement': 'right'
          });
          /* x-editable jquery plugin: pronounced 'sheditable' */
          $.fn.editable.defaults.mode = 'popup';
          $('.xeditable').editable({
              url: $setVal,
              emptytext: "Click to edit",
              params: function (params) {
                  params.table = $(this).attr("data-table");
                  params.user_id = $(this).attr("data-cid");
                  params.name = $(this).attr("data-field");
                  params.pk = $(this).attr("data-pk");
                  return params
              },
              display: function(value, response) {
                  //disable this method so we can update in 'success' method
                  return false;
              },
              success: function(response, newValue) {
                  $.growlUI('Success', "Data saved.");
                  $icon = $(this).find("i");
                  if ($icon.attr("data-content") == '') {
                      $icon.attr("class",'fa fa-commenting green');
                  }
                  if (newValue == "") {
                      $icon.attr("class",'fa fa-commenting-o green');
                  }else{
                      $icon.attr("class",'fa fa-commenting red');
                  }
                  $icon.attr("data-content", newValue);
                  $(this).find("span").text(newValue);
              }
          });
      }
  });
  $( "#students-toggle" ).on('submit', function(e) {
    if ($('#athletes-print').is(":checked")) {
      return true;
    } else {
      $.ajax({
          type: "POST",
          url: $getStudents,
          data: $("#students-toggle").serialize(),
          cache: false,
          beforeSend: function(){
          // disable form submit button
              $('#submit-toggle').attr('disabled', 'disabled');
              spinner.spin(target);
          },
          success: function(data) {
              spinner.stop(target);
              // enable form submit button
              $('#submit-toggle').removeAttr('disabled');
              if (data != "error") {
                  $("#students-data-panel").html(data);
                  // initialise the datatable
                  var table = $('#students-data').DataTable({
                    buttons: [
                        {
                            text: 'CSV',
                            extend: 'csv',
                            fieldSeparator: '|',
                            extension: '.csv'
                        },
                        'excel'
                    ],
                    dom: 'lfrBtip',
                    order: [[4, "asc"]],
                    lengthMenu: [
                      [100, 250, 500, 1000, 2000, -1],
                      [100, 250, 500, 1000, 2000, "All"]
                    ],
                    drawCallback: function() {
                      $('[data-toggle="popover"]').popover({
                          trigger: 'hover',
                          'placement': 'right'
                      });
                      /* x-editable jquery plugin: pronounced 'sheditable' */
                      $.fn.editable.defaults.mode = 'popup';
                      $('.xeditable').editable({
                          url: $setVal,
                          emptytext: "Click to edit",
                          params: function (params) {
                            params.table = $(this).attr("data-table");
                            params.user_id = $(this).attr("data-cid");
                            params.name = $(this).attr("data-field");
                            params.pk = $(this).attr("data-pk");
                            return params
                          },
                          display: function(value, response) {
                            //disable this method so we can update in 'success' method
                            return false;
                          },
                          success: function(response, newValue) {
                            $.growlUI('Success', "Data saved.");
                            $icon = $(this).find("i");
                            if ($icon.attr("data-content") == '') {
                                $icon.attr("class",'fa fa-commenting green');
                            }
                            if (newValue == "") {
                                $icon.attr("class",'fa fa-commenting-o green');
                            }else{
                                $icon.attr("class",'fa fa-commenting red');
                            }
                            $icon.attr("data-content", newValue);
                            $(this).find("span").text(newValue);
                          }
                      });
                    }
                  });
                  $('#students-data').on( 'click', 'tr', function () {
                      if ( $(this).hasClass('selected') ) {
                          $(this).removeClass('selected');
                      } else {
                          table.$('tr.selected').removeClass('selected');
                          $(this).addClass('selected');
                      }
                  });
                  $('#students-data').on( 'change', 'input', function () {
                      var $dis = $(this);
                      var $data = {
                          'user_id': $dis.attr("data-cid"),
                          'value': $dis.val(),
                          'name': $dis.attr("name"),
                          'table': $dis.attr("data-table"),
                          'pk': $dis.attr("data-pk")
                      }
                      $.ajax({
                          type: "POST",
                          url: $setVal,
                          data: $data,
                          cache: false,
                          beforeSend: function(){
                              spinner.spin(target);
                          },
                          success: function(data) {
                              spinner.stop(target);
                              if (data == "success") {
                                  check ='<i class="fa fa-check"></i>';
                                  $dis.replaceWith(check);
                                  $.growlUI('Success', "Data saved.");
                              } else {
                                  $.growlUI('Error?', data);
                              }
                          },
                          error: function(data) {
                              spinner.stop(target);
                              $.growlUI('Error?', data);
                          }
                      });
                  });
              } else {
                  alert("There was a problem retrieving the data.\n\
                  Please execute your search again.");
              }
          }
      });
      return false;
    }
  });
  $('#students-data').on( 'click', 'tr', function () {
      if ( $(this).hasClass('selected') ) {
          $(this).removeClass('selected');
      } else {
          table.$('tr.selected').removeClass('selected');
          $(this).addClass('selected');
      }
  });
  $('#students-data').on( 'change', 'input', function () {
      var $dis = $(this);
      var $data = {
          'user_id': $dis.attr("data-cid"),
          'value': $dis.val(),
          'name': $dis.attr("name"),
          'table': $dis.attr("data-table"),
          'pk': $dis.attr("data-pk")
      }
      $.ajax({
          type: "POST",
          url: $setVal,
          data: $data,
          cache: false,
          beforeSend: function(){
              spinner.spin(target);
          },
          success: function(data) {
              spinner.stop(target);
              if (data == "success") {
                  check ='<i class="fa fa-check"></i>';
                  $dis.replaceWith(check);
                  $.growlUI('Success', "Data saved.");
              } else {
                  $.growlUI('Error?', data);
              }
          },
          error: function(data) {
              spinner.stop(target);
              /* does not work */
              $('div.growlUI').addClass('gerror');
              $.growlUI('Error?', data);
          }
      });
  });
});
