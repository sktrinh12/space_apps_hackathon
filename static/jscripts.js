$(document).ready(function() {

  $('#form-impute').submit(function (event) {
      event.preventDefault();
        $('div#plot-content').empty();
        $.ajax({
        url:"/updatePlot_impute/",
        dataType:'json',
        success: function(reply) {

          var figure_impute = $(reply.html_plot);
          $('div#plot-content').html(figure_impute);
        },
        error: function(reply) {
          alert('error:' + reply);
        }
        })
   });

   $('#form-upload').submit(function (event) {
      event.preventDefault();
        $('div#plot-content').empty();
        $.ajax({
        url:"/updatePlot_raw/",
        dataType:'json',
        success: function(reply) {

          var figure_up = $(reply.html_plot);
          $('div#plot-content').html(figure_up);
        }
        })
   });

   $('#form-ml').submit(function (event) {
      event.preventDefault();
        $('div#plot-content').empty();
        $.ajax({
        url:"/updatePlot_ml/",
        dataType:'json',
        success: function(reply) {

          var figure_ml = $(reply.html_plot);
          $('div#plot-content').html(figure_ml);
        }
        })
   });

});
