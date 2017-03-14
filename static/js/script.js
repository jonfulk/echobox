$(document).ready(function() {

  function update_total() {
    $.getJSON($SCRIPT_ROOT + "/_total",
      function(data) {
        $("#total").text(data.echoes);
      });
  }

  function go(url) {
    $.ajax({
      url: url
    })
    .done(function() {
      console.log('done!');
      update_total();
    });
  }

  $('.delete-this').on('click', function(e) {
    e.preventDefault();
    var url = $(this).attr('href')
    $(this).parent().fadeOut(700, function() {
      go(url);
    });
  })

});
