import app_globals
import web

from pymongo import Connection
from pymongo.objectid import ObjectId
from view import render
from myrequest import Request
import nltk

from db import User, Job, session, sql_db as db
import sphinxapi 
urls = (
    '/search', 'search',
    '/view/(.*)', 'view',
    '/sortby/(.*)', 'sortby'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)

class search(object):
   
    def POST(self):
        u = Request().POST
        
        cl = sphinxapi.SphinxClient()
        cl.SetServer("127.0.0.1", 3312)
        cl.SetMatchMode(sphinxapi.SPH_MATCH_ALL)
        cl.SetSortMode(sphinxapi.SPH_SORT_RELEVANCE)
        res = cl.Query(u['searchd'])
        ids = res['matches']
        
        #ids_list = []
        #if ids: 
        #    ids_list = [('obj_data', self._sku_info(i['id'])) for i in ids]
  
        #return ids_list
        #return render('search_results.mako', rp=ids_list, search_term=u['searchd'])
        print self._sku_info(7420957, search_term='cams skunk2')
       
    def _sku_info(self, post_id, search_term):

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
                    AND SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) = %s 
                    AND listings_posts.list_starter = 1 
                """ % (post_id)

        rp = db.bind.execute(sql)

        storage = {}
        for num, entry in enumerate(rp.fetchall()):
            storage = {
                #'post_id' : entry[0], 
                #'title' : entry[1],
                #'list_id' : entry[2],
                #'text' : nltk.sent_tokenize(entry[4]),
                #'srch_trm' : search_term.split(" "),
                'matches' : self._determine_match(nltk.sent_tokenize(entry[4]), search_term.split(" "))
            }

        return storage

    def _determine_match(self, text, search_term):
        storage = []
        for term in search_term:
            matches = [sent for sent in text if term in sent.lower()]
            for match in matches:
                storage.append({
                    'term' : match,
                    'match' : term
                })

        return storage
 
class view(object):
    def GET(self, list_id):
        sql = """
            SELECT   
                data_prep.list_title AS title
              , listings_posts.list_text_html AS html
              , listings_posts.list_author AS auth
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
