# -------------------
# Imports
# -------------------

from flask import Flask, render_template, request
import json
from requests import get

# -------------------
# Init
# -------------------

app = Flask(__name__)

# -------------------
# Routes
# -------------------

@app.route('/')
def index():
  org_name = request.args.get('organization_name')
  return render_template('index.html', org_name=org_name)

@app.route('/find', methods=['POST'])
def find():
  '''
  Finds issues based on the given label
  '''
  org_name = request.form.get('org_name', None)

  labels = request.form['labels']
  labels.replace(' ', '')

  if org_name != 'None':
    issues = get('http://localhost:5000/api/organizations/%s/issues/labels/%s?per_page=100' % (org_name, labels))
  else:
    issues = get('http://localhost:5000/api/issues/labels/'+labels+'?per_page=100')

  issues = json.loads(issues.content)

  return render_template('index.html', issues=issues['objects'], labels=request.form['labels'], org_name=org_name)


if __name__ == "__main__":
    app.run(debug=True, port=4000)