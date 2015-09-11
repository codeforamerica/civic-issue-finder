# -------------------
# Imports
# -------------------

from flask import Flask, render_template, request, jsonify
import json, time, os
from urlparse import urljoin
from operator import itemgetter

from uritemplate import expand
from requests import get
from requests.exceptions import ConnectionError, Timeout

from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build

# -------------------
# Init
# -------------------

app = Flask(__name__,  static_folder='static', static_url_path='/geeks/civicissues/static')
app.secret_key = os.environ['SECRET']

# Variables
CFAPI_BASE = 'https://www.codeforamerica.org/api/'
GOOGLE_ANALYTICS_PROFILE_ID = "41226190"
GOOGLE_SERVICE_ACCOUNT_EMAIL = os.environ["GOOGLE_SERVICE_ACCOUNT_EMAIL"]
GOOGLE_SERVICE_ACCOUNT_SECRET_KEY = os.environ["GOOGLE_SERVICE_ACCOUNT_SECRET_KEY"]

#
# Setup for all GA queries
#
def login_to_google_analytics():
    credentials = SignedJwtAssertionCredentials(GOOGLE_SERVICE_ACCOUNT_EMAIL, GOOGLE_SERVICE_ACCOUNT_SECRET_KEY,
    'https://www.googleapis.com/auth/analytics.readonly')
    http = Http()
    credentials.authorize(http)
    service = build("analytics", "v3", http=http)
    return service, credentials.access_token

service, access_token = login_to_google_analytics()


# DATA FUNCTIONS
def get_total_clicks():
    ''' Get the total clicks from Google Analytics '''
    results = service.data().ga().get(
          ids="ga:" + GOOGLE_ANALYTICS_PROFILE_ID,
          start_date='2014-08-23',
          end_date='today',
          metrics='ga:totalEvents',
          dimensions=None,
          sort=None,
          max_results=None,
          filters='ga:eventCategory==Civic Issues',
          fields=None).execute()

    total_clicks = results["rows"][0][0]
    return total_clicks


def get_total_views():
    ''' Get the total views from Google Analytics '''
    results = service.data().ga().get(
          ids="ga:" + GOOGLE_ANALYTICS_PROFILE_ID,
          start_date='2014-08-23',
          end_date='today',
          metrics='ga:pageviews',
          dimensions=None,
          sort=None,
          max_results=None,
          filters='ga:pagePath=@civicissues',
          fields=None).execute()

    total_views = results["rows"][0][0]
    return total_views


def get_weekly_clicks():
    ''' Get Weekly clicks as a list of lists '''
    results = service.data().ga().get(
          ids="ga:" + GOOGLE_ANALYTICS_PROFILE_ID,
          start_date='2014-08-23',
          end_date='today',
          metrics='ga:totalEvents',
          dimensions='ga:yearWeek',
          sort=None,
          max_results=None,
          filters='ga:eventCategory==Civic Issues',
          fields=None).execute()

    weekly = results['rows']
    for week in weekly:
        week[0] = str(week[0])
        week[1] = int(week[1])
    # weekly = [ list( map( int, week ) ) for week in weekly ]
    return weekly


def get_top_embeds():
    ''' Get top embed sources '''
    results = service.data().ga().get(
          ids="ga:" + GOOGLE_ANALYTICS_PROFILE_ID,
          start_date='2014-08-23',
          end_date='today',
          metrics='ga:totalEvents',
          dimensions='ga:eventLabel',
          sort='-ga:totalEvents',
          max_results=1000,
          filters='ga:eventCategory==Civic Issue View',
          fields=None).execute()

    sources = []
    for result in results['rows']:
        source = result[0].split(',')[1]
        if source != "None":
            if '?' in source:
                source = source.split('?')[0]
            source = source.split("://")[1]
            sources.append(source)

    top_embeds = []
    for source in sources:
        source_count = [str(source), sources.count(source)]
        if source_count not in top_embeds:
            top_embeds.append(source_count)

    top_embeds = sorted(top_embeds, key=itemgetter(1), reverse=True)

    return top_embeds

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


@app.route("/geeks/civicissues/analytics")
def analytics():

    # Get Total Clicks
    total_clicks = get_total_clicks()
    total_views = get_total_views()
    clicks_per_view = int(100 * int(total_clicks)/float(int(total_views)))
    weekly = get_weekly_clicks()
    # embeds = get_top_embeds()

    return render_template("analytics.html", total_clicks=total_clicks,
            total_views=total_views, clicks_per_view=clicks_per_view,
            weekly=weekly)


@app.route("/geeks/civicissues/analytics/total_clicks")
def total_clicks():
    ''' Return total clicks as json '''
    total_clicks = get_total_clicks()
    response = {
      "total_clicks" : total_clicks
    }
    return json.dumps(response)



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
