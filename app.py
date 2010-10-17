#!/usr/bin/env python
import web
import app_globals

from view import render 
from forms import LoginAccountForm, CreateAccountForm
from myrequest import Request
from SprocketAuth import SprocketAuth

from db import User, Job, session, sql_db as db

import welcome, site_admin, masthead, header, job, parts

web.config.debug = True

urls = (
    '/', 'index',
    '/maro/(.*)', 'hkro',
    '/login', 'login',
    '/logout', 'logout',
    '/create_account', 'create_account',
    '/welcome', welcome.app,
    '/site', site_admin.app,
    '/job', job.app, 
    '/parts', parts.app
)

app = web.application(urls, globals(), autoreload=True)
 
sa = SprocketAuth(app)

class index(object):
    def GET(self):
        sql = """SELECT * FROM site"""
        sites = db.bind.execute(sql)
        return render('index.mako', sites=sites)

class create_account(object):
    @sa.protect()
    def GET(self): pass

    def POST(self): 
        login  = LoginAccountForm()
        create = CreateAccountForm(Request().POST) 
        if create.validate() != True:
            return render('index.mako', login=login, create=create)
        return web.input()
 
class logout(object):
    def GET(self):
        sa.logout()
        return web.seeother('../')

class login(object):

    def POST(self):    
        login  = LoginAccountForm(Request().POST)
        create = CreateAccountForm() 
        if login.validate() != True: 
            return render('site_admin.mako', site_type='login', login=login, create=create)

        post = web.input()
        import hashlib
        psswrd = hashlib.sha1(post.password).hexdigest()
        query = db.users.filter_by(name=post.username, password=psswrd).first()
    
        if query:
            user = query.id
        else:
            user = False

        return sa.login({ 
            'check' : query,
            'redirect_to_if_pass' : '../welcome/',
            'redirect_to_if_fail' : '../',
            'user' : user
        })

class maro(object):
    def GET(self, name):
        return masthead.index().GET()

if __name__ == "__main__":
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
