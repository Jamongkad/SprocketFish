import app_globals
import web

from view import render
from myrequest import Request
from forms import LoginAccountForm, CreateAccountForm
import masthead

urls = (
    '/', 'index',
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class index(object):
    def GET(self):

        login = LoginAccountForm()
        create = CreateAccountForm()
        mast = masthead.index().GET('Mathew')
        logged_in = web.ctx.session.get('loggedIn')

        return render('header.mako', login=login, create=create, mast=mast, logged_in=logged_in)

