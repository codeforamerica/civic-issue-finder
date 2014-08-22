function update_snippet () {
  var labels = document.getElementById('labels').value;
  var org = document.getElementById('organization').value;
  var code = document.getElementById('embed');
  var widget = document.getElementById('widget');

  if (org !== '') {
    if (labels !== '') {
      embed_string = '&lt;iframe src="http://civicissues.herokuapp.com/widget?organization_name='+ encodeURIComponent(org) +'&labels='+ labels.trim() +'" width="100%" height="600" frameBorder="0"&gt; &lt;/iframe&gt;';
      widget.src = 'http://civicissues.herokuapp.com/widget?organization_name='+ encodeURIComponent(org) +'&labels='+ labels.trim();
    } else{
      embed_string = '&lt;iframe src="http://civicissues.herokuapp.com/widget?organization_name='+ encodeURIComponent(org) +'" width="100%" height="600" frameBorder="0"&gt; &lt;/iframe&gt;';
      widget.src = 'http://civicissues.herokuapp.com/widget?organization_name='+ encodeURIComponent(org);
    };
  } else if (labels !== '') {
    embed_string = '&lt;iframe src="http://civicissues.herokuapp.com/widget?labels='+ labels.trim() +'" width="100%" height="600" frameBorder="0"&gt; &lt;/iframe&gt;';
    widget.src = 'http://civicissues.herokuapp.com/widget?labels='+ labels.trim();
  } else {
    embed_string = '&lt;iframe src="http://civicissues.herokuapp.com/widget" width="100%" height="600" frameBorder="0"&gt; &lt;/iframe&gt;';
    widget.src = 'http://civicissues.herokuapp.com/widget';
  };
  code.innerHTML = embed_string;


}

var labels = document.getElementById('labels');
var org = document.getElementById('organization');

org.addEventListener('change', update_snippet);
labels.addEventListener('keyup', update_snippet);
