$(document).ready(function () {
  $("#id_title").autocomplete(
    '/ajax/action/autocomplete/',
    { multiple: false, multipleSeparator: ' '}
  );
});