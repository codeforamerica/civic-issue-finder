# -------------------
# Imports
# -------------------

from flask import Flask, render_template, request, redirect, url_for
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
  return render_template('index.html')


@app.route('/embed')
def embed():
    '''
    Show an editable embed form
    '''

    # Get all of the organizations from the api
    organizations = get('http://codeforamerica.org/api/organizations?per_page=200')
    organizations = organizations.json()

    # Filter out just the organization names
    names = []
    for org in organizations['objects']:
        names.append(org['name'])

    # Alphabetize names
    names.sort()

    # Render index and pass in all of the organization names
    return render_template('embed.html', organization_names=names)


@app.route('/widget')
def widget():
  '''
  Finds issues based on the given label. Render them in the widget
  '''
  # Get optional parameters
  labels = request.args.get('labels', None)
  org_name = request.args.get('organization_name')

  # Get the actual issues from the API
  try:
    # If we have an organization name only query that organization
    if org_name != None:
      if labels != None:
        issues = get('http://codeforamerica.org/api/organizations/%s/issues/labels/%s' % (org_name, labels))
      else:
        issues = get('http://codeforamerica.org/api/organizations/%s/issues' % org_name)
    # Otherwise get issues across all organizations
    else:
      if labels != None:
        issues = get('http://codeforamerica.org/api/issues/labels/%s' % labels)
      else:
        issues = get('http://codeforamerica.org/api/issues')
  except ConnectionError, e:
    return render_template('widget.html', error=True)

  if issues.status_code != 200:
    return render_template('widget.html', error=True)

  # Parse the API response
  issues = issues.json()
  issues = issues['objects']

  # Format each issue
  for issue in issues:
    # Add text_color to labels to make them more readable
    for label in issue['labels']:
      if label['color'] < '888888':
        label['text_color'] = 'FFFFFF'
      else:
        label['text_color'] = '000000'

  return render_template('widget.html', issues=issues, labels=labels)

if __name__ == "__main__":
    app.run(debug=True)
