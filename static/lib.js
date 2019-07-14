/*
 * Set the textContent of elementId to the responseText.
 */
function updateStatus(eId, r) {
  var el = document.getElementById(eId);
  el.textContent = "Status:" + r.status + " statusText:" + r.statusText + " responseText:" + r.responseText;
}
