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
        ids_list = []
        if ids: 
            for i in ids:
                ids_list.append(i['id'])

        string = [str(x) for x in ids_list] 
        bunch =  ", ".join(string)
        sql = """select 
                    SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) AS post_id
                  , data_prep.list_title AS title
                  , listings_posts.idlistings_posts AS list_id
                  , data_prep.list_sku AS sku
                  , listings_posts.list_text_text AS text
                  , listings_posts.list_text_html AS html
                  , listings_posts.list_author AS auth
                from 
                    data_prep 
                INNER JOIN
                    listings_posts
                    ON data_prep.list_sku = listings_posts.list_sku
                where 1=1 
                    AND SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1)  IN (%s)
                GROUP BY
                    sku
                ORDER BY 
                    sku DESC""" % (bunch)

        rp = db.bind.execute(sql)
        return rp.fetchall()

        


