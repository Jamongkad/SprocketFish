import web

from helpers.view import render
from helpers.myrequest import Request
from helpers.forms import LoginAccountForm, CreateAccountForm
from modules.masthead.controllers import masthead
urls = (
    '/', 'index',
)

app = web.application(urls, globals(), autoreload=True)
from helpers.SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class index(object):
    def GET(self):
        login = LoginAccountForm()
        create = CreateAccountForm()
        mast = masthead.index().GET('Mathew')
        logged_in = web.ctx.session.get('loggedIn')
        return render('header.mako', login=login, create=create, mast=mast, logged_in=logged_in)

