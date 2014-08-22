function update_snippet () {
  var labels = document.getElementById('labels').value;
  var org = document.getElementById('organization').value;
  var code = document.getElementById('embed');
  var widget = document.getElementById('widget');

  if (org !== '') {
    if (labels !== '') {
      embed_string = '&lt;iframe src="http://codeforamerica.org/geeks/civicissues/widget?organization_name='+ encodeURIComponent(org) +'&labels='+ labels.trim() +'" width="100%" height="600" frameBorder="0"&gt; &lt;/iframe&gt;';
      widget.src = 'http://codeforamerica.org/geeks/civicissues/widget?organization_name='+ encodeURIComponent(org) +'&labels='+ labels.trim();
    } else{
      embed_string = '&lt;iframe src="http://codeforamerica.org/geeks/civicissues/widget?organization_name='+ encodeURIComponent(org) +'" width="100%" height="600" frameBorder="0"&gt; &lt;/iframe&gt;';
      widget.src = 'http://codeforamerica.org/geeks/civicissues/widget?organization_name='+ encodeURIComponent(org);
    };
  } else if (labels !== '') {
    embed_string = '&lt;iframe src="http://codeforamerica.org/geeks/civicissues/widget?labels='+ labels.trim() +'" width="100%" height="600" frameBorder="0"&gt; &lt;/iframe&gt;';
    widget.src = 'http://codeforamerica.org/geeks/civicissues/widget?labels='+ labels.trim();
  } else {
    embed_string = '&lt;iframe src="http://codeforamerica.org/geeks/civicissues/widget" width="100%" height="600" frameBorder="0"&gt; &lt;/iframe&gt;';
    widget.src = 'http://codeforamerica.org/geeks/civicissues/widget';
  };
  code.innerHTML = embed_string;


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
