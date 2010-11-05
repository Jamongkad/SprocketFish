import app_globals
import web

from pymongo import Connection
from pymongo.objectid import ObjectId
from view import render
from myrequest import Request
import nltk, itertools, string, MultiDict, pprint
from SkuInfo import SkuInfo

from db import sql_db as db
import sphinxapi 
urls = (
    '/search', 'search',
    '/view/(.*)', 'view',
    '/sortby/(.*)', 'sortby',
    '/browse', 'browse'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class search(object):

    def GET(self):
        u = web.input()
        search_query = u['searchd']

        sk = SkuInfo()
        res = sk.cl.Query(search_query)

        ids = res['matches']
        
        ids_list = []
        if ids: 
            ids_list = [sk.sku_info(i['id'], search_query) for i in ids]
 
        return render('search_results.mako', rp=ids_list, search_term=search_query)
    
class view(object):
    def GET(self, list_id):
        sql = """
            SELECT   
                data_prep.list_title AS title
              , listings_posts.list_text_html AS html
              , listings_posts.list_author AS auth
              , DATE_FORMAT(data_prep.list_date, GET_FORMAT(DATE, 'USA')) AS date
            FROM 
                data_prep
            INNER JOIN
                listings_posts
                ON data_prep.list_sku = listings_posts.list_sku
            where 1=1 
                AND data_prep.list_sku = '%s'
                AND listings_posts.list_starter = 1 
        """ % (list_id) 
        rp = db.bind.execute(sql)
        return render('part_view.mako', rp=rp.fetchall())

class sortby(object):
    def GET(self, site_id):
        sql = """
            SELECT 
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
                AND SUBSTRING_INDEX(data_prep.list_sku, ":", 1) = '%s'
                AND listings_posts.list_starter = 1 
        """ % (site_id) 
        rp = db.bind.execute(sql)
        return rp.fetchall()

class browse(object):
    def GET(self):
        from pagination import Pagination
        pg = Pagination(15, 100, '/parts/browse_view')
        return pg.buildLinks()
        #import datetime
        #sk = SkuInfo()
        #sql = """
        #    SELECT 
        #        SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) AS post_id
        #      , data_prep.list_title AS title
        #      , listings_posts.idlistings_posts AS list_id
        #      , data_prep.list_sku AS sku
        #      , listings_posts.list_text_text AS text
        #      , listings_posts.list_text_html AS html
        #      , listings_posts.list_author AS auth
        #    FROM 
        #        data_prep
        #    INNER JOIN
        #        listings_posts
        #        ON data_prep.list_sku = listings_posts.list_sku
        #    WHERE 1=1
        #        AND listings_posts.list_starter = 1 
        #        AND data_prep.list_date = '%s'
        #""" % (datetime.date.today().isoformat()) 

        #br = db.bind.execute(sql)  
        #ids_list = [sk.sku_info(i['post_id'], i['title']) for i in br.fetchall()] 
        #return render('browse_view.mako', rp=ids_list) 

def matrank(weight, num_of_photos):
    return weight + num_of_photos * 0.00001
