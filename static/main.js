// Resize iframe to fit content
function resize() {
  var newheight = document.getElementById("widget").contentWindow.document.body.scrollHeight;
  document.getElementById("widget").height = newheight + "px";
}
