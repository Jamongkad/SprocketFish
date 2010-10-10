import web

class SprocketAuth(object):

    def __init__(self, app):
        self.main_app = app
        self.session = web.session.Session(self.main_app, web.session.DiskStore('sessions'))

        def session_hook():
            web.ctx.session = self.session

        self.main_app.add_processor(web.loadhook(session_hook))

    def protect(self, redirect=False): 
        def meth_signature(meth):
            def new(*args, **kwa):
                if web.ctx.session.get('loggedIn') is True:
                    print "get %s" % (web.ctx.session)
                    return meth(*args, **kwa)
                if redirect is False:
                    return web.seeother(web.ctx.homedomain) 
                return web.seeother(redirect)
            return new
        return meth_signature

    def login(self, login_vars):  
        if login_vars.get('check'):
            web.ctx.session.loggedIn = True
            web.ctx.session.user_id  = login_vars.get('user')
            if login_vars.get('redirect_to_if_pass'):
                print "set %s" % (web.ctx.session)
                raise web.seeother(login_vars.get('redirect_to_if_pass'))
                #return "passed redirect to %s" % (login_vars.get('redirect_to_if_pass')), web.ctx.session
            else:
                print "could not set session"
                raise web.seeother(web.ctx.homedomain)
                #return "passed but no redirect provided"
        else:
            raise web.seeother(web.ctx.homedomain) 
            #return "failed completely"

    def logout(self):  
        web.ctx.session.loggedIn = False
