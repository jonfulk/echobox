$(document).ready(function() {

  function update_total(count) {
    $("#total").text(count);
  }

  function deleteEcho(url) {
    $.ajax({
      url: url
    })
    .success(function(result) {
      update_total(result.echoes);
    });
  }

  $('.delete-this').on('click', function(e) {
    e.preventDefault();
    var url = $(this).attr('href')
    $(this).parent().fadeOut(700, function() {
      deleteEcho(url);
    });
  })

});
