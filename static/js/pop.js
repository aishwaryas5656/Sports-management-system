$('button[name="remove_levels"]').on('click', function(e) {
  var $form = $(this).closest('form');
  e.preventDefault();
  $('#confirm').modal({
      backdrop: 'static',
      keyboard: false
  })
  .on('click', '#delete', function(e) {
      $form.trigger('submit');
    });
  $("#cancel").on('click',function(e){
   e.preventDefault();
   $('#confirm').modal.model('hide');
  });
});