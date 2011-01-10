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

import parts_model, redis, cPickle

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
cache_timeout = 1800 #30mins

class search(object):

    def GET(self):
        u = web.input()
        search_query = u['searchd']

        if not search_query: 
            raise web.seeother('../')

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
                ids_list = cPickle.loads(str(ids_list_redis))
            else: 
                print "set cache:search_results"
                ids_list = sk.sku_info(id_select, search_query)
                ids_list_for_cache = cPickle.dumps(ids_list)
                r_server.set("search_results:%s" % search_query, ids_list_for_cache)

        r_server.expire("search_results:%s" % search_query, cache_timeout) 
        return render('search_results.mako', rp=ids_list, search_term=search_query)
 
class view(object):
    def GET(self):
        u = web.input()   

        pg   = 'pg=' + u['pg'] if 'pg' in u else ''
        sl   = '&sl=' + u['sl'] if 'sl' in u else ''
        img  = '&with_img=' + u['with_img'] if 'with_img' in u else ''
        srch = u['searchd'] if 'searchd' in u else None

        rp = parts_model.Sites().view_entry(u['list_id'])
        return render('part_view.mako', rp=rp.fetchall(), pg=pg, sl=sl, img=img, srch=srch)

class browse(object):
    def GET(self):
        u = web.input()
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

        values = {'site_select': site_select, 'img': img_post_ids}

        sql_rows = """
            SELECT 
                SQL_CALC_FOUND_ROWS
                list_title 
            FROM 
                data_prep AS dp
            INNER JOIN
                listings_posts AS lp
                    ON lp.list_sku = dp.list_sku 
            WHERE 1=1
                AND SUBSTRING_INDEX(dp.list_sku, ":", 1) IN (%(site_select)s)
                %(img)s
            GROUP BY 
                list_title 
        """ % (values)
        res_rows = db.bind.execute(sql_rows)  
        
        sql_foundRows = text("""SELECT FOUND_ROWS() as foundRows""")
        
        #total_entries_select_key = "foundrows:%s" % (":".join(sites_for_now))
        #if r_server.get(total_entries_select_key): 
        #    print "cache_hit:browsedate-foundrows:retrieve"
        #    total_entries = cPickle.loads(r_server.get(total_entries_select_key))
        #else: 
        #    print "cache_hit:browsedate-foundrows:set"
        #    res = db.bind.execute(sql)
        #    total_entries = res.fetchall()[0][0]
        #    r_server.set(total_entries_select_key, cPickle.dumps(total_entries))
       
        res_foundRows = db.bind.execute(sql_foundRows)
        total_entries = res_foundRows.fetchall()

        return res_rows.fetchall()
       
        pg = Pageset(total_entries, 50)
        pg.current_page(current_page)
        date_sql = """
                SELECT 
                    dp.list_date AS list_date
                  , dp.list_title AS title
                  , dp.list_sku AS sku 
                  , SUBSTRING_INDEX( SUBSTRING_INDEX(lp.idlistings_posts, ':', 2), ':', -1) AS post_id
                FROM 
                    /*
                    (SELECT 
                         list_sku 
                       , list_title
                       , list_date
                     FROM 
                         data_prep
                     WHERE 1=1
                         AND SUBSTRING_INDEX(list_sku, ":", 1) IN (%(site_select)s)
                    ) AS dp
                    */
                    data_prep AS dp
                INNER JOIN
                    /*
                    (SELECT
                         idlistings_posts
                       , list_sku
                       , list_starter
                     FROM
                         listings_posts
                     WHERE 1=1
                         AND list_starter = 1 
                    ) AS lp
                    */
                    listings_posts AS lp
                        ON lp.list_sku = dp.list_sku 
                WHERE 1=1
                    %(img)s
                    AND SUBSTRING_INDEX(dp.list_sku, ":", 1) IN (%(site_select)s)
                    AND lp.list_starter = 1
                ORDER BY
                    list_date DESC
                LIMIT %(offset)i, %(limit)i
                """ % ({'site_select': site_select, 'img': img_post_ids,  'offset': pg.skipped(), 'limit': pg.entries_per_page()}) 

        option_select_key = "%s:%s:%s" % (":".join(sites_for_now), pg.skipped(), pg.entries_per_page())
        option_select_key_browse = "%s:%s:%s:browse" % (":".join(sites_for_now), pg.skipped(), pg.entries_per_page())

        if r_server.get(option_select_key): 
            print "cache_hit:browsedata-date:retrieve"
            date_result = cPickle.loads(str(r_server.get(option_select_key)))
        else:
            print "cache_hit:browsedata-date:set"
            date_result = db.bind.execute(date_sql).fetchall()
            r_server.set(option_select_key, cPickle.dumps(date_result))
 
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

        if r_server.get(option_select_key_browse): 
            print "cache_hit:browsedata-browse:retrieve"
            d = cPickle.loads(str(r_server.get(option_select_key_browse)))
        else:
            print "cache_hit:browsedata-browse:set"
            d = OrderedDict()
            for i in date_result:
                d.setdefault(i[0], [])
                d[i[0]].append((i[1], i[2]))
            r_server.set(option_select_key_browse, cPickle.dumps(d))
          
        r_server.expire(option_select_key, cache_timeout)        
        r_server.expire(option_select_key_browse, cache_timeout)        
        #r_server.expire(total_entries_select_key, cache_timeout)

        #r_server.delete(option_select_key)
        #r_server.delete(option_select_key_browse)
        #r_server.delete(total_entries_select_key)

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
