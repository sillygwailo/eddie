function search_submit() {
  var query = $("#id_query").val();
  $("#search-results").load(
    "/search/?ajax&query="+encodeURIComponent(query)
  );
  page = 'search';
  history.pushState(page, query, '/search/?query='+encodeURIComponent(query));
  return false;
}
$(document).ready(function () {
  $("#search-form").submit(search_submit);
})