import os
import chat
import unittest
import tempfile


class ChatTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, chat.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = chat.app.test_client()
        chat.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(chat.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Unbelievable. No entries here so far'.encode() in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('Zahar', 'z-1996')
        assert 'You were logged in'.encode() in rv.data
        rv = self.logout()
        assert 'You were logged out'.encode() in rv.data
        rv = self.login('Kolya', 'z-1996')
        assert 'Invalid username'.encode() in rv.data
        rv = self.login('Zahar', '122')
        assert 'Invalid password'.encode() in rv.data

    def test_messages(self):
        self.login('Zahar', 'z-1996')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far'.encode() not in rv.data
        assert '&lt;Hello&gt;'.encode() in rv.data
        assert '<strong>HTML</strong> allowed here'.encode() in rv.data


if __name__ == '__main__':
    unittest.main()
