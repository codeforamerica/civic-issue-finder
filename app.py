# -------------------
# Imports
# -------------------

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json, time
from requests import get
from requests.exceptions import ConnectionError

# -------------------
# Init
# -------------------

app = Flask(__name__,  static_folder='static', static_url_path='/geeks/civicissues/static')

# -------------------
# Routes
# -------------------

@app.route('/geeks/civicissues')
def index():
    return render_template('index.html')


@app.route('/geeks/civicissues/embed')
def embed():
    '''
    Show an editable embed form
    '''

    # Get all of the organizations from the api
    organizations = get('http://codeforamerica.org/api/organizations.geojson')
    organizations = organizations.json()

    # Filter out just the organization names
    names = []
    for org in organizations['features']:
        names.append(org['properties']['name'])

    # Alphabetize names
    names.sort()

    # Render index and pass in all of the organization names
    return render_template('embed.html', organization_names=names)


@app.route('/geeks/civicissues/widget')
def widget():
    '''
    Finds issues based on the given label. Render them in the widget
    '''
    # Get optional parameters
    labels = request.args.get('labels', None)
    org_name = request.args.get('organization_name')
    org_type = request.args.get('org_type')
    number = request.args.get('number')

    # Build the url
    issues_url = 'http://codeforamerica.org/api/'
    if org_name:
        issues_url += 'organizations/%s/' % org_name
    issues_url += 'issues'
    if labels:
        issues_url += '/labels/%s' % labels
    if org_type:
        issues_url += '?organization_type=%s' % org_type
        if number:
            issues_url += '&per_page=%s' % number
    elif number:
        issues_url += '?per_page=%s' % number

    # Get the actual issues from the API
    try:
        issues_response = get(issues_url)
    except ConnectionError, e:
        return render_template('widget.html', error=True)

    if issues_response.status_code != 200:
        return render_template('widget.html', error=True)

    # Parse the API response
    issues_json = issues_response.json()
    issues = issues_json['objects']

    return render_template('widget.html', issues=issues, labels=labels)

@app.route("/geeks/civicissues/.well-known/status")
def engine_light():
    ''' Return status information for Engine Light.
        http://engine-light.codeforamerica.org
    '''

    status = "ok"

    # Check if GitHub avatars are loading.
    response = get("https://avatars.githubusercontent.com/u/595778?v=2&s=40")
    if response.status_code != 200:
        status = "GitHub Avatars not loading."

    # Check if CfAPI is up.
    response = get("http://codeforamerica.org/api/issues")
    if response.status_code != 200:
        status = "CfAPI not returning Issues."

    state = {

        "status" : status,
        "updated" : int(time.time()),
        "resources" : [],
        "dependencies" : ['Github', 'CfAPI']
    }

    return jsonify(state)

if __name__ == "__main__":
    app.run(debug=True)
