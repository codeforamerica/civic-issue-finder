function update_snippet () {
  var labels = document.getElementById('labels').value;
  var org = document.getElementById('organization').value;
  var code = document.getElementById('embed');
  if (org !== '') {
    if (labels !== '') {
      embed_string = '&lt;iframe src="http://civicissues.herokuapp.com/widget?organization_name='+ encodeURIComponent(org) +'&default_labels='+ labels.trim() +'" width="300" height="600"&gt; &lt;/iframe&gt;';
    } else{
      embed_string = '&lt;iframe src="http://civicissues.herokuapp.com/widget?organization_name='+ encodeURIComponent(org) +'" width="300" height="600"&gt; &lt;/iframe&gt;';
    };
  } else if (labels !== '') {
    embed_string = '&lt;iframe src="http://civicissues.herokuapp.com/widget?default_labels='+ labels.trim() +'" width="300" height="600"&gt; &lt;/iframe&gt;';
  };
  code.innerHTML = embed_string;
}

var labels = document.getElementById('labels');
var org = document.getElementById('organization');

org.addEventListener('change', update_snippet);
labels.addEventListener('keyup', update_snippet);

console.log('holaa');