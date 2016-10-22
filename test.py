import os
import unittest

from HoverSpace.application import app
from HoverSpace.models import DATABASE as db
from pymongo import MongoClient

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        db.drop_database('hoverspace')

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def signup(self, username, password, email, firstname, lastname):
        return self.app.post('/signup', data=dict(
            username=username,
            password=password,
            email=email,
            firstname=firstname,
            lastname=lastname,
            ), follow_redirects=True)

    def test_login_logout_signup(self):
        rv = self.login('vidhan', 'qwerty')
        assert b'Wrong username or password!\n' in rv.data

        rv = self.signup('vidhan13', 'rrxstssr', 'axyz@gmail.com', 'ronchi', 'johanson')
        assert b'SignUp successfull!' in rv.data

        rv = self.login('vidhan13', 'rrxstssr')
        assert b'Logged in successfully!' in rv.data

        rv = self.logout()
        assert b'Login' in rv.data

        rv = self.signup('vidhan14', 'rrxstssrr', 'axyz@gmail.com', 'ronchii', 'johansonn')
        assert b'You have already signed up from this email id\n' in rv.data

if __name__ == '__main__':
    unittest.main()
