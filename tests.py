#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest

from httmock import response, HTTMock, all_requests
from flask.ext.testing import TestCase
from app import app
import flask

class AppTestCase(TestCase):

    def create_app(self):
        # This method is required by flask.ext.testing.TestCase. It is called
        # before setUp().
        return app

    @all_requests
    def response_content(self, url, request):
        if url.geturl() == 'https://publicmedia-cfapi.herokuapp.com/api/organizations?per_page=200':
            return response(200, ''' {"objects":[{"name":"Code for America"}]} ''' )

        elif url.geturl() == 'https://publicmedia-cfapi.herokuapp.com/api/organizations/Code-for-America/issues':
            return response(200, ''' {"objects":[{"html_url":"https://github.com/TESTORG/TESTREPO/issues/1","project":{"github_details":{"contributors":[{"avatar_url":"https://TESTIMAGEURL.com"}]}},"title":"TEST TITLE"}]}''')

        elif url.geturl() == 'https://publicmedia-cfapi.herokuapp.com/api/issues/labels/help%20wanted,enhancement':
            return response(200, ''' {"objects":[{"html_url":"https://github.com/TESTORG/TESTREPO/issues/1","labels":[{"name": "help wanted"},{"name": "enhancement"}],"project":{"github_details":{"contributors":[{"avatar_url":"https://TESTIMAGEURL.com"}]}},"title":"TEST TITLE"}]}''')

        elif url.geturl() == 'https://publicmedia-cfapi.herokuapp.com/api/issues':
            return response(200, ''' {"objects":[{"html_url":"https://github.com/TESTORG/TESTREPO/issues/1","labels":[],"project":{"github_details":{"contributors":[{"avatar_url":"https://TESTIMAGEURL.com"}]}},"title":"TEST TITLE"}]}''')

        elif url.geturl() == 'https://publicmedia-cfapi.herokuapp.com/api/issues?per_page=2':
            return response(200, ''' {"objects":[{"html_url":"https://github.com/TESTORG/TESTREPO/issues/1","labels":[],"project":{"github_details":{"contributors":[{"avatar_url":"https://TESTIMAGEURL.com"}]}},"title":"TEST TITLE"}, {"html_url":"https://github.com/TESTORG/TESTREPO/issues/2","labels":[],"project":{"github_details":{"contributors":[{"avatar_url":"https://TESTIMAGEURL.com"}]}},"title":"TEST TITLE TWO"}]}''')

    def test_widget(self):
        with HTTMock(self.response_content):
            response = self.client.get('/geeks/civicissues/widget')
            assert 'https://github.com/TESTORG/TESTREPO/issues/1' in response.data
            assert '<h3 class="billboard-label">TEST TITLE</h3>' in response.data
            assert 'class="label"' not in response.data

    def test_embed_org_names(self):
        with HTTMock(self.response_content):
            response = self.client.get('/geeks/civicissues/embed')
            assert '<option value="Code for America">Code for America</option>' in response.data

    def test_widget_org_name(self):
        with HTTMock(self.response_content):
            response = self.client.get('/geeks/civicissues/widget?organization_name=Code-for-America')
            assert 'https://github.com/TESTORG/TESTREPO/issues/1' in response.data
            assert '<h3 class="billboard-label">TEST TITLE</h3>' in response.data

    def test_widget_labels(self):
        with HTTMock(self.response_content):
            response = self.client.get('/geeks/civicissues/widget?labels=help wanted,enhancement')
            assert '<div class="labels">' in response.data
            assert '<div class="label">help wanted</div>' in response.data
            assert '<div class="label">enhancement</div>' in response.data

    def test_widget_number(self):
        with HTTMock(self.response_content):
            response = self.client.get('/geeks/civicissues/widget?number=2')
            assert (response.data.count('<li class="layout-crotchet">') == 2)

    def test_widget_tracking(self):
        with HTTMock(self.response_content):
            response = self.client.get('/geeks/civicissues/widget?tracking=false')
            self.assertTrue("GoogleAnalyticsObject" not in response.data)

if __name__ == '__main__':
    unittest.main()