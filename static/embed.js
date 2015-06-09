function updateSnippet () {
  var labels = document.getElementById('labels').value;
  var org = document.getElementById('organization').value;
  org = org.replace(/ /g, '-');
  var code = document.getElementById('embed');
  var widget = document.getElementById('widget');
  var number = document.getElementById('number');

  var embedString = 'https://www.codeforamerica.org/geeks/civicissues/widget';
  if (org || labels || number){
    embedString += '?'
  }
  if (org) {
    embedString += 'organization_name=' + org;
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
  embedString = '<iframe src="' + embedString + '" width="100%" height="600" frameBorder="0"></iframe>';
  code.innerHTML = embedString;
}

window.onload = function() {

  var labels = document.getElementById('labels');
  var organization = document.getElementById('organization');

  organization.addEventListener('change', updateSnippet);
  labels.addEventListener('change', updateSnippet);
  number.addEventListener('change', updateSnippet);

}