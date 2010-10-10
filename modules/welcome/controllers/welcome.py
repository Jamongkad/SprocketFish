import app_globals
import web

from sqlalchemy import or_, and_, desc
from view import render
from forms import AddJob
from db import User, Job, session, sql_db as db
from myrequest import Request

from mx.DateTime import DateTime

urls = (
    '/', 'index',
    '/add_job', 'add_job',
    '/create_account', 'create_account'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class index(object):
    @sa.protect()
    def GET(self):   
        user_id = web.ctx.session.user_id
        name = db.users.filter_by(id=user_id).first().name
        jobs = db.jobs.order_by(desc(db.jobs.job_id)).all()
        job_form = AddJob()  
        return render('welcome.mako', name=name, jobs=jobs, job_form=job_form)

      
class add_job(object):
    def POST(self):
        i = web.input()
        job_form = AddJob(Request().POST)

        user_id = web.ctx.session.user_id
        name = db.users.filter_by(id=user_id).first().name
        jobs = db.jobs.all()

        if job_form.validate() is True:
            start_date = i.start_date.split("/")
            day   = int(start_date[0])
            month = int(start_date[1])
            year  = int(start_date[2])
            time  = DateTime(year, month, day, 0, 0, 0)

            db.jobs.insert(job_nm=i.job_name, job_desc=i.job_desc, job_date_start=time.ticks())
            try:
                db.commit()
            except:
                db.rollback()

            web.redirect('../welcome/')
        else:
            return render('welcome.mako', name=name, jobs=jobs, job_form=job_form)

