import app_globals
import web

from pymongo import Connection
from pymongo.objectid import ObjectId
from view import render
from myrequest import Request
import nltk, itertools, string, MultiDict, pprint
from SkuInfo import SkuInfo

from paginate import Pageset
from ordereddict import OrderedDict
import datetime, MultiDict 

from db import sql_db as db
import sphinxapi 
urls = (
    '/search', 'search',
    '/view/(.*)', 'view',
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


class browse(object):
    def GET(self):
        u = web.input()
        pg, sl = u['pg'] if 'pg' in u else None, u['sl'] if 'sl' in u else None 

        current_page = int(pg) 
        sites = ["'HCP'", "'GT'", "'JDMU'", "'MLPH'"]

        if sl != None:
            sites = []
            for site in sl.split(","):
                sites.append("'%s'" % site)
         
        site_select = ",".join(sites)

        sql = """
            SELECT 
                SQL_CALC_FOUND_ROWS
                list_title 
            FROM 
                data_prep 
            WHERE 1=1
                AND DATE_FORMAT(list_date, '%s') = "2010"
                AND SUBSTRING_INDEX(data_prep.list_sku, ":", 1) IN (%s)
            GROUP BY 
                list_title 
        """ % ('%%Y', site_select)
        db.bind.execute(sql)  
        
        sql = """SELECT FOUND_ROWS() as foundRows"""

        res = db.bind.execute(sql)
        total_entries = res.fetchall()[0][0]
        pg = Pageset(total_entries, 100)
        pg.current_page(current_page)
        date_sql = """
                SELECT 
                    data_prep.list_date AS list_date
                  , data_prep.list_title AS title
                  , data_prep.list_sku AS sku 
                  , SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) AS post_id
                FROM 
                    data_prep
                INNER JOIN
                    listings_posts
                    ON data_prep.list_sku = listings_posts.list_sku
                WHERE 1=1
                    AND listings_posts.list_starter = 1 
                    AND DATE_FORMAT(list_date, '%s') = "2010" 
                    AND SUBSTRING_INDEX(data_prep.list_sku, ":", 1) IN (%s)
                GROUP BY
                    title
                ORDER BY
                    list_date DESC
                LIMIT %d, %d
                """ % ('%%Y', site_select, pg.skipped(), pg.entries_per_page())

        date_result = db.bind.execute(date_sql).fetchall()
        pages = pg.pages_in_set()
        first = pg.first_page()
        last  = pg.last_page()          
             
        d = OrderedDict()
        for i in date_result:
            d.setdefault(i[0], [])
            d[i[0]].append((i[1], i[2]))

        return render('browse_view.mako', pages=pages, date_result=d, first=first, last=last, current_page=current_page, sl=sl)  
       

def matrank(weight, num_of_photos):
    return weight + num_of_photos * 0.00001


#date_sql = """
#    SELECT 
#        list_date
#      , ds.title
#      , ds.sku
#      , ds.post_id
#    FROM 
#        data_prep AS dp
#    INNER JOIN ( 
#        SELECT 
#            SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) AS post_id
#          , data_prep.list_title AS title
#          , listings_posts.idlistings_posts AS list_id
#          , data_prep.list_sku AS sku
#          , listings_posts.list_text_text AS text
#          , listings_posts.list_text_html AS html
#          , listings_posts.list_author AS auth
#          , data_prep.list_date AS date
#          , SUBSTRING_INDEX(data_prep.list_sku, ":", 1) AS site_id
#        FROM 
#            data_prep
#        INNER JOIN
#            listings_posts
#            ON data_prep.list_sku = listings_posts.list_sku
#        WHERE 1=1
#            AND listings_posts.list_starter = 1 
#    ) AS ds
#        ON ds.date = dp.list_date
#    WHERE 1=1
#        AND DATE_FORMAT(list_date, '%s') = "2010" 
#        AND ds.site_id IN (%s)
#    GROUP BY 
#        ds.title 
#    ORDER BY
#        list_date DESC
#    LIMIT %d, %d
#""" % ('%%Y', site_select, pg.skipped(), pg.entries_per_page())
