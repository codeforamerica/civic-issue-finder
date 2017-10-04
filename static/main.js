// Function to retrieve document height
function getDocumentHeight(doc) {
  var doc = doc || document;
  var body = doc.body, html = doc.documentElement;
  var height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
  return height;
}
// Resize iframe to fit content
function resize() {
  var ifrm = document.getElementById('widget');
  var doc = ifrm.contentDocument ? ifrm.contentDocument : ifrm.contentWindow.document;
  ifrm.style.visibility = 'hidden';
  ifrm.style.height = "10px";
  ifrm.style.height = getDocumentHeight(doc) + 4 + "px";
  ifrm.style.visibility = 'visible';
}
