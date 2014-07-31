# -------------------
# Imports
# -------------------

from flask import Flask, render_template, request
import json
from requests import get
from requests.exceptions import ConnectionError

# -------------------
# Init
# -------------------

app = Flask(__name__)

# -------------------
# Routes
# -------------------

@app.route('/')
def index():
  names = []
  # Get all of the organizations from the api
  organizations = get('http://codeforamerica.org/api/organizations?per_page=200')
  organizations = json.loads(organizations.content)

  # Filter out just the organization names
  for org in organizations['objects']:
    names.append(org['name'])

  # Render index and pass in all of the organization names
  return render_template('index.html', organization_names=names)

@app.route('/widget')
def widget():
  '''
  Render the basic empty widget
  '''
  org_name = request.args.get('organization_name')
  default_labels = request.args.get('default_labels')
  return render_template('widget.html', org_name=org_name, default_labels=default_labels, main=True)

@app.route('/find', methods=['POST'])
def find():
  '''
  Finds issues based on the given label. Render them in the widget
  '''
  # Get optional parameters
  org_name = request.form.get('org_name', "None")
  default_labels = request.form.get('default_labels', "None")

  # Get labels from form
  labels = request.form['labels']

  # Include optional labels
  if default_labels != 'None':
    default_labels.replace(' ', '')
    labels += ',' + default_labels

  # Remove possible whitespace (ex: "enhancement, hack")
  labels.replace(' ', '')

  # Get the actual issues from the API
  try:
    # If we have an organization name only query that organization
    if org_name != 'None':
      issues = get('http://codeforamerica.org/api/organizations/%s/issues/labels/%s?per_page=100' % (org_name, labels))
    # Otherwise get issues across all organizations
    else:
      issues = get('http://codeforamerica.org/api/issues/labels/'+labels+'?per_page=100')
  except ConnectionError, e:
    return render_template('index.html', org_name=org_name, default_labels=default_labels, error=True)

  if issues.status_code != 200:
    return render_template('index.html', org_name=org_name, default_labels=default_labels, error=True)

  # Parse the API response
  issues = json.loads(issues.content)  

  # Add text_color for each issue
  for iss in issues['objects']:
    for l in iss['labels']:
      if l['color'] < '888888':
        l['text_color'] = 'FFFFFF'
      else:
        l['text_color'] = '000000'

  return render_template('widget.html', issues=issues['objects'], labels=request.form['labels'], org_name=org_name, default_labels=default_labels)

if __name__ == "__main__":
    app.run(debug=True)