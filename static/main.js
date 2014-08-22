function updateSnippet () {
  var labels = document.getElementById('labels').value;
  var org = document.getElementById('organization').value;
  var code = document.getElementById('embed');
  var widget = document.getElementById('widget');
  var number = document.getElementById('number');

  var embedString = 'http://codeforamerica.org/geeks/civicissues/widget';
  if (org || labels || number){
    embedString += '?'
  }
  if (org) {
    embedString += 'organization_name=' + encodeURIComponent(org);
    if (labels || number){
      embedString += '&';
    }
  }
  if (labels) {
    embedString += 'labels=' + labels.trim();
    if (number) {
      embedString += '&';
    }
  }
  if (number) {
    embedString += 'number=' + number.value;
  }

  // Reload the iframe
  widget.src = embedString;

  // Finish the embedString for the form
  embedString = '&lt;iframe src="' + embedString + '" width="100%" height="600" frameBorder="0"&gt; &lt;/iframe&gt;';
  code.innerHTML = embedString;
}

window.onload = function() {

  var labels = document.getElementById('labels');
  var organization = document.getElementById('organization');

  organization.addEventListener('change', update_snippet);
  labels.addEventListener('keyup', update_snippet);

}

// Resize iframe to fit content
function resize() {
  var newheight = document.getElementById("widget").contentWindow.document.body.scrollHeight;
  document.getElementById("widget").height = newheight + "px";
}
