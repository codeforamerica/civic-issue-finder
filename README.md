Civic Issue Finder
=====

A small, embedable and customizable web app to find civic issues to work on based on their issues. It fetches data from the [Code for America API](http://codeforamerica.org/api).

How to Use
======

This widget can be [accessed directily](http://civicissues.herokuapp.com), or it can be embeded into any webpage with the following code:

```html
<iframe src="http://civicissues.herokuapp.com?default_labels=hack" width='300' height='400'></iframe>
```

The url in the `src` attribute of the iframe can be given the following query params to cutomize your widget

- `organization_name`: Only looks for issues of projects in the given organization. The organization has to be inside the CFAPI. Here's a [list of organizations](http://codeforamerica.org/api/organizations)
- `default_labels`: Labels that should always be included in the search query.