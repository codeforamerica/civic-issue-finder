# -------------------
# Imports
# -------------------

from flask import Flask, render_template, request, jsonify
import json, time, os
from urlparse import urljoin

from uritemplate import expand
from requests import get
from requests.exceptions import ConnectionError, Timeout

# -------------------
# Init
# -------------------

app = Flask(__name__,  static_folder='static', static_url_path='/geeks/civicissues/static')
app.secret_key = os.environ['SECRET']

CFAPI_BASE = 'https://www.codeforamerica.org/api/'

# -------------------
# Routes
# -------------------

@app.route('/geeks/civicissues')
def index():
    header = get("http://www.codeforamerica.org/fragments/global-header.html")
    footer = get("http://www.codeforamerica.org/fragments/global-footer.html")
    return render_template('index.html', header=header.content, footer=footer.content)


@app.route('/geeks/civicissues/embed')
def embed():
    '''
    Show an editable embed form
    '''

    header = get("http://www.codeforamerica.org/fragments/global-header.html")
    footer = get("http://www.codeforamerica.org/fragments/global-footer.html")

    # Get all of the organizations from the api
    try:
        got = get(urljoin(CFAPI_BASE, 'organizations.geojson'), timeout=5)
    except Timeout:
        return render_template('cfapi-timeout.html')
    else:
        organizations = got.json()

    # Filter out just the organization names
    names = []
    for org in organizations['features']:
        names.append(org['properties']['name'])

    # Alphabetize names
    names.sort()

    # Render index and pass in all of the organization names
    return render_template('embed.html', organization_names=names, header=header.content, footer=footer.content)


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
    tracking_status = request.args.get('tracking')

    # Build the url
    if org_name and labels:
        issues_path_template = 'organizations{/org_name}/issues/labels{/labels}{?query*}'
    elif org_name:
        issues_path_template = 'organizations{/org_name}/issues{?query*}'
    elif labels:
        issues_path_template = 'issues/labels{/labels}{?query*}'
    else:
        issues_path_template = 'issues{?query*}'
        
    issues_url_template = urljoin(CFAPI_BASE, issues_path_template)
    issues_url_kwargs = ('organization_type', org_type), ('per_page', number)
    
    url_args = dict(org_name=org_name, labels=labels,
                    query={k:v for (k, v) in issues_url_kwargs if v})
    
    issues_url = expand(issues_url_template, url_args)

    # Get the actual issues from the API
    try:
        issues_response = get(issues_url, timeout=5)
    except Timeout:
        return render_template('widget.html', error=True)
    except ConnectionError, e:
        return render_template('widget.html', error=True)

    if issues_response.status_code != 200:
        return render_template('widget.html', error=True)

    # Parse the API response
    issues_json = issues_response.json()
    issues = issues_json['objects']

    return render_template('widget.html', issues=issues,
            referrer=request.referrer, tracking_status=tracking_status)


@app.route("/geeks/civicissues/.well-known/status")
def engine_light():
    ''' Return status information for Engine Light.
        http://engine-light.codeforamerica.org
    '''

    status = "ok"

    # Check if GitHub avatars are loading.
    try:
        response = get("https://avatars.githubusercontent.com/u/595778?v=2&s=40", timeout=5)
    except:
        status = "GitHub Avatars not loading."
    else:
        if response.status_code != 200:
            status = "GitHub Avatars not loading."

    # Check if CfAPI is up.
    try:
        response = get(urljoin(CFAPI_BASE, 'issues?per_page=1'), timeout=5)
    except:
        status = "CfAPI not returning Issues."
    else:
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
