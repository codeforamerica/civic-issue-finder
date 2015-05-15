# -------------------
# Imports
# -------------------

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json, time, uuid, os
from urlparse import urljoin

from uritemplate import expand
from psycopg2 import connect
from requests import get
from requests.exceptions import ConnectionError

# -------------------
# Init
# -------------------

app = Flask(__name__,  static_folder='static', static_url_path='/geeks/civicissues/static')
app.secret_key = os.environ['SECRET']
DATABASE_URL = os.environ['DATABASE_URL']

CFAPI_BASE = 'https://www.codeforamerica.org/api/'

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
    organizations = get('https://www.codeforamerica.org/api/organizations.geojson')
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
        issues_response = get(issues_url)
    except ConnectionError, e:
        return render_template('widget.html', error=True)

    if issues_response.status_code != 200:
        return render_template('widget.html', error=True)

    # Parse the API response
    issues_json = issues_response.json()
    issues = issues_json['objects']
    
    referer = request.headers.get('Referer', '')

    return render_template('widget.html', issues=issues, labels=labels,
                           referer=referer, tracking_status=tracking_status)



@app.route('/geeks/civicissues/issue/<issue_id>')
def one_issue(issue_id):
    ''' Redirect to an issue's HTML URL.
    '''
    issue_url = 'https://www.codeforamerica.org/api/issues/{}'.format(issue_id)
    
    if 'visitor_id' not in session:
        session['visitor_id'] = str(uuid.uuid4())
    
    timestamp = time.time()
    remote_addr = request.remote_addr
    visitor_id = session['visitor_id']
    referer = request.args.get('referer', '')
    
    with connect(DATABASE_URL) as conn:
        with conn.cursor() as db:
            db.execute('''INSERT INTO issue_clicks
                          (datetime, remote_addr, visitor_id, referer, issue_url)
                          VALUES (to_timestamp(%s), %s, %s, %s, %s)''',
                       (timestamp, remote_addr, visitor_id, referer, issue_url))
    
    return redirect(get(issue_url).json().get('html_url'))

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
    response = get("https://www.codeforamerica.org/api/issues?per_page=1")
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
