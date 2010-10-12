import app_globals
import web

from pymongo import Connection
from pymongo.objectid import ObjectId
from view import render
from myrequest import Request

from db import User, Job, session, sql_db as db
import sphinxapi

urls = (
    '/search', 'search',
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class search(object):
    def POST(self):
        u = Request().POST
        
        cl = sphinxapi.SphinxClient()
        cl.SetServer("127.0.0.1", 3312)
        res = cl.Query(u['searchd'])
        ids = res['matches']

        if ids: 
            ids_list = [i['id'] for i in ids]

        bunch =  ", ".join( [str(x) for x in ids_list] )
        sql = """SELECT 
                    SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) AS post_id
                  , data_prep.list_title AS title
                  , listings_posts.idlistings_posts AS list_id
                  , data_prep.list_sku AS sku
                  , listings_posts.list_text_text AS text
                  , listings_posts.list_text_html AS html
                  , listings_posts.list_author AS auth
                FROM 
                    data_prep 
                INNER JOIN
                    listings_posts
                    ON data_prep.list_sku = listings_posts.list_sku
                where 1=1 
                    AND SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1)  IN (%s)
                    AND listings_posts.list_starter = 1
                ORDER BY 
                    sku DESC""" % (bunch)

        rp = db.bind.execute(sql)
        return render('search_results.mako', rp=rp, search_term=u['searchd'])
        

        


