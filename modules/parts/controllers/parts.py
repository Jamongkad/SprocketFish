import app_globals
import web

from pymongo import Connection
from pymongo.objectid import ObjectId
from view import render
from SkuInfo import SkuInfo

from paginate import Pageset
from ordereddict import OrderedDict
import datetime

from db import sql_db as db, text
import sphinxapi 

import parts_model, redis, pickle

urls = (
    '/search', 'search',
    '/view', 'view',
    '/browse', 'browse',
    '/test', 'test'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)
r_server = redis.Redis("localhost")

class search(object):

    def GET(self):
        u = web.input()
        cache_time = 1800
        search_query = u['searchd']

        sk = SkuInfo()
        res = sk.cl.Query(search_query)

        ids = res['matches']
        
        collected_ids = [str(i['id']) for i in ids]
        id_select = ','.join(collected_ids)
        
        ids_list = None
        if ids: 
            if r_server.get("search_results:%s" % search_query):
                print "from cache:search_results"
                ids_list_redis = r_server.get("search_results:%s" % search_query)
                ids_list = pickle.loads(ids_list_redis)
            else: 
                print "set cache:search_results"
                ids_list = sk.sku_info(id_select, search_query)
                ids_list_for_cache = pickle.dumps(ids_list)
                r_server.set("search_results:%s" % search_query, ids_list_for_cache)

        r_server.expire("search_results:%s" % search_query, cache_time)
       
        return render('search_results.mako', rp=ids_list, search_term=search_query)

    
class view(object):
    def GET(self):
        u = web.input()   

        pg   = 'pg=' + u['pg'] if 'pg' in u else ''
        sl   = '&sl=' + u['sl'] if 'sl' in u else ''
        img  = '&with_img=' + u['with_img'] if 'with_img' in u else ''
        srch = u['searchd'] if 'searchd' in u else None

        sql = text("""
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
                AND data_prep.list_sku = :x
                AND listings_posts.list_starter = 1 
        """) 
        rp = db.bind.execute(sql, x=u['list_id'])
        return render('part_view.mako', rp=rp.fetchall(), pg=pg, sl=sl, img=img, srch=srch)

class browse(object):
    def GET(self):
        u = web.input()

        cache_time = 1800

        pg, sl, with_img = u['pg'] if 'pg' in u else None, u['sl'] if 'sl' in u else None, u['with_img'] if 'with_img' in u else None

        current_page = int(pg) 
        sites_for_now = parts_model.Sites().show_sites() 

        if sl:
            new_sites = []
            for site in sl.split(","):
                new_sites.append("'%s'" % site)

            sites_for_now = new_sites
                       
        site_select = ",".join(sites_for_now)

        img_post_ids = ''
        if with_img:
            sk = SkuInfo()
            sk.cl.SetLimits(0, 1000)
            res = sk.cl.Query('.jpg')
            img_post = [("'%s'" % i['id']) for i in res['matches']]
            img_post_ids = "AND SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) IN (" + ",".join(img_post) + ")"

        values = {'year': '%%Y', 'site_select': site_select, 'img': img_post_ids}

        sql = """
            SELECT 
                SQL_CALC_FOUND_ROWS
                list_title 
            FROM 
                data_prep 
            INNER JOIN
                listings_posts
                    ON data_prep.list_sku = listings_posts.list_sku
            WHERE 1=1
                AND DATE_FORMAT(list_date, '%(year)s') = "2010"
                AND SUBSTRING_INDEX(data_prep.list_sku, ":", 1) IN (%(site_select)s)
                %(img)s
            GROUP BY 
                list_title 
        """ % (values)
        db.bind.execute(sql)  
        
        sql = text("""SELECT FOUND_ROWS() as foundRows""")

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
                    AND DATE_FORMAT(list_date, '%(year)s') = "2010" 
                    AND SUBSTRING_INDEX(data_prep.list_sku, ":", 1) IN (%(site_select)s)
                    %(img)s
                GROUP BY
                    title
                ORDER BY
                    list_date DESC
                LIMIT %(offset)i, %(limit)i
                """ % ({'year': '%%Y', 'site_select': site_select, 'img': img_post_ids,  'offset': pg.skipped(), 'limit': pg.entries_per_page()})
        


        if r_server.get("date_result"):
            print "from cache:date_result"
            date_result_redis = r_server.get("date_result")
            date_result = pickle.loads(date_result_redis)
        else:
            print "set cache:date_result"
            date_result = db.bind.execute(date_sql).fetchall()
            date_pickle = pickle.dumps(date_result) 
            r_server.set("date_result", date_pickle)
          
        pages = pg.pages_in_set()
        first = pg.first_page()
        last  = pg.last_page()          
        
        sites_alpha = parts_model.Sites().show_sites(with_quotes=False) 
        chosen = []
        if sl:
            chosen = sl.split(',')                    
        
        if chosen != None:
            remaining = filter(lambda x : x not in chosen, sites_alpha)
        else:
            remaining = sites_alpha

        selected = filter(lambda x : x in chosen, sites_alpha)
        
        connect_str = "" if len(selected) == 1 or len(selected) == 0 else "&sl="
        img_str = "&with_img=1" if with_img else ""
        img_str_sl = "&sl=" if len(selected) > 0 else ""

        #d = OrderedDict()
        #for i in date_result:
        #    d.setdefault(i[0], [])
        #    d[i[0]].append((i[1], i[2]))
        if r_server.get("browse_data"):
            print "from cache:browse_data"
            browse_result_redis = r_server.get("browse_data")
            d = pickle.loads(browse_result_redis)
        else: 
            print "set cache:browse_data"
            d = OrderedDict()
            for i in date_result:
                d.setdefault(i[0], [])
                d[i[0]].append((i[1], i[2]))
            d_browse_data = pickle.dumps(d)
            r_server.set("browse_data", d_browse_data)

        r_server.expire("date_result", cache_time)
        r_server.expire("browse_data", cache_time)
        
        #r_server.delete("date_result")
        #r_server.delete("browse_data")

        return render('browse_view.mako', pages=pages, date_result=d, first=first, 
                      last=last, current_page=current_page, sl=sl, with_img=with_img,
                      chosen=chosen, remaining=remaining, selected=selected, connect_str=connect_str, img_str_sl=img_str_sl, img_str=img_str)  

class test(object):
    def GET(self):
        sk = SkuInfo()
        sk.cl.SetLimits(0, 1000)
        res = sk.cl.Query('.jpg|img')
        img_post = [("'%s'" % i['id']) for i in res['matches']]
        img_post_ids = ",".join(img_post)
        return img_post_ids


def matrank(weight, num_of_photos):
    return weight + num_of_photos * 0.00001
