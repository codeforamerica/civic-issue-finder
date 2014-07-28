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
  return render_template('index.html')

@app.route('/find', methods=['POST'])
def find():
  '''
  Finds issues based on the given label
  '''
  labels = request.form['labels']
  labels.replace(' ', '')

  issues = get('http://localhost:5000/api/issues/labels/'+labels+'?per_page=100')
  print issues.content
  issues = json.loads(issues.content)

  return render_template('index.html', issues=issues['objects'], labels=request.form['labels'])


if __name__ == "__main__":
    app.run(debug=True, port=4000)