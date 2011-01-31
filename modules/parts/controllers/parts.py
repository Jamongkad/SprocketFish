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

import parts_model, redis, cPickle, re

urls = (
    '/search', 'search',
    '/view', 'view',
    '/browse', 'browse',
    '/mark', 'mark',
    '/test', 'test'
)

app = web.application(urls, globals(), autoreload=True)
from SprocketAuth import SprocketAuth
sa = SprocketAuth(app)
r_server = redis.Redis("localhost")
cache_timeout = 3600 #1hour

class search(object):

    def GET(self):
        u = web.input()
        search_query = u['searchd']
        auth = u['auth'] if 'auth' in u else None
        site = u['site'] if 'site' in u else None

        if 'pg' in u:
            page_num = u['pg']
        else:
            page_num = 0

        id_select      = None
        srch_term_sphx = None
        display_term   = None
        num_rows       = None
        time           = None
        limit          = 20

        if not search_query: 
            raise web.seeother('../')

        sc = sphinxapi.SphinxClient()
        sc.SetServer("127.0.0.1", 3312)
        sc.SetMatchMode(sphinxapi.SPH_MATCH_ALL)
        sc.SetSortMode(sphinxapi.SPH_SORT_RELEVANCE)
        sc.SetSortMode(sphinxapi.SPH_SORT_ATTR_DESC, 'post_date')
        sc.SetLimits(int(page_num) * 10, limit)

        def get_collected_ids(sq):
            res = sc.Query(sq, index="posts")
            matched_ids = res['matches']
            total_found = res['total_found'] 
            collected_ids = [str(i['id']) for i in matched_ids]
            id_select = ','.join(collected_ids)

            return id_select, total_found

        def getID(cleansed_ids, sql_type=False):
            if sql_type is "site_nm":
                sql_id = """SELECT site_id FROM site WHERE site_nm IN (%(site_select)s)""" % ({'site_select': cleansed_ids})

            if sql_type is "auth_nm":
                sql_id = """SELECT auth_id FROM author WHERE auth_nm IN (%(auth_select)s)""" % ({'auth_select': cleansed_ids})

            id_rows = db.bind.execute(sql_id)
            return [int(i[0]) for i in id_rows]

        def splitify(target_id, key=False):
            if target_id:
                t_id = dict([(i.strip().split(":")[0], i.strip().split(":")[1]) for i in re.split('(@[a-zA-Z]+(:[a-zA-Z,-_|]+))', target_id) if re.search('@(\w+)', i)]) 
                if key in t_id:
                    return t_id[key].split("|")
               
        search_query = search_query.strip()
        if re.compile('(@[a-zA-Z]+)').findall(search_query):            
            print "advance query"
            srch_terms = re.split('(@[a-zA-Z]+(:[a-zA-Z,-_|]+))', search_query)
            terms = [i.strip() for i in srch_terms if not re.search('(:\w+)', i)]
            terms = [i for i in terms if i]
            terms = terms[0] if terms else ""

            siteid = splitify(site, key="@site")
            authid = splitify(auth, key="@auth")
            #srch_ttle = "@title " + " ".join(srch_hash['@title'].split(",")) if '@title' in srch_hash else None
            #srch_body = "@body " + " ".join(srch_hash['@body'].split(",")) if '@body' in srch_hash else None
            site_ids_db = getID(",".join(["'%s'" % i.upper() for i in siteid]), sql_type="site_nm") if siteid else None
            auth_ids_db = getID(",".join(["'%s'" % i for i in authid]), sql_type="auth_nm") if authid else None
            
            if siteid and site_ids_db:
                print "filtering by site ids"
                sc.SetFilter('site_id', site_ids_db)
     
            if authid and auth_ids_db:
                print "filtering by auth ids"
                sc.SetFilter('auth_id', auth_ids_db)

            srch_term_sphx = terms
            display_term = search_query 
            gci = get_collected_ids(srch_term_sphx)
            id_select = gci[0]
            num_rows = gci[1]
        else:
            print "basic query"
            srch_term_sphx = search_query
            display_term = search_query
            gci = get_collected_ids(search_query)
            id_select = gci[0]
            num_rows = gci[1]

        pg = Pageset(num_rows, limit)
        pg.current_page(pg)
        
        pages = pg.pages_in_set()
        first = pg.first_page()
        last  = pg.last_page()                  
 
        sk = SkuInfo()
        ids_listinfo = sk.sku_info(id_select, srch_term_sphx, sc) if id_select else None

        return render('search_results.mako', rp=ids_listinfo, search_term=display_term, pages=pages, first=first, last=last, current_page=int(page_num) 
                      , limit=limit, auth=auth, site=site, num_rows=num_rows)
        """ 
        ids_list = None

        search_set_redis = "-".join(search_query.split(" "))
        
        if ids: 
            if r_server.get("search_results:%s:%s:%s" % (search_set_redis, forum, author)):
                print "from cache:search_results"
                ids_list_redis = r_server.get("search_results:%s:%s:%s" % (search_set_redis, forum, author))
                ids_list = cPickle.loads(str(ids_list_redis))
            else: 
                print "set cache:search_results"
                ids_list = sk.sku_info(id_select, search_query, sc)
                ids_list_for_cache = cPickle.dumps(ids_list)
                r_server.set("search_results:%s:%s:%s" % (search_set_redis, forum, author), ids_list_for_cache)

        r_server.expire("search_results:%s" % search_set_redis, cache_timeout) 
        """ 

class view(object):
    
    def GET(self):
        u = web.input()   

        pg   = 'pg=' + u['pg'] if 'pg' in u else ''
        sl   = '&sl=' + u['sl'] if 'sl' in u else ''
        img  = '&with_img=' + u['with_img'] if 'with_img' in u else ''
        srch = u['searchd'] if 'searchd' in u else None

        rp = parts_model.Sites().view_entry(u['list_id'])
        return render('part_view.mako', rp=rp.fetchall(), pg=pg, sl=sl, img=img, srch=srch, list_id=u['list_id'])

class mark(object):
    def GET(self):
        u = web.input()
        return u['list_id'], u['type']

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

        img_post_ids = ""
        if with_img:
            sk = SkuInfo()
            sk.cl.SetLimits(0, 1000)
            res = sk.cl.Query('.jpg')
            img_post = [("'%s'" % i['id']) for i in res['matches']]
            img_post_ids = "AND SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) IN (" + ",".join(img_post) + ")"

        values = {'site_select': site_select, 'img': img_post_ids} 
        sc = sphinxapi.SphinxClient()
        sc.SetServer("127.0.0.1", 3312)
        #sc.SetSortMode(sphinxapi.SPH_SORT_ATTR_DESC, "post_date")

        sql_id = """SELECT site_id FROM site WHERE site_nm IN (%(site_select)s)""" % ({'site_select': site_select})
        id_rows = db.bind.execute(sql_id)
        site_ids = [int(i[0]) for i in id_rows] 
        limit = 50

        sc.SetFilter('site_id', site_ids)
        #sc.SetLimits(int(pg) * 10, limit)
        res = sc.Query("")
        num_rows = res['total_found'] 

        pg = Pageset(num_rows, limit)
        pg.current_page(current_page)

        option_select_key = "%s:%s:%s" % (":".join(sites_for_now), pg.skipped(), pg.entries_per_page())
        option_select_key_browse = "%s:%s:%s:browse" % (":".join(sites_for_now), pg.skipped(), pg.entries_per_page())

        #sk = SkuInfo()
        #ids_list = sk.sku_info(','.join([str(i['id']) for i in res['matches']]), None, sc)
       
       # d = OrderedDict()
       # for i in ids_list:
       #     d.setdefault(i['date'], [])
       #     d[i['date']].append((i['title'], i['sku']))
      
        if r_server.get(option_select_key): 
            print "cache_hit:browsedata-date:retrieve"
            date_result = cPickle.loads(str(r_server.get(option_select_key)))
        else:
            print "cache_hit:browsedata-date:set"
            date_sql = """
                     SELECT 
                        dp.list_date AS list_date
                      , dp.list_title AS title
                      , dp.list_sku AS sku 
                      , SUBSTRING_INDEX( SUBSTRING_INDEX(lp.idlistings_posts, ':', 2), ':', -1) AS post_id
                    FROM (
                        SELECT
                            list_date,
                            list_title,
                            list_sku
                        FROM
                            data_prep                             
                        WHERE 1=1
                            AND SUBSTRING_INDEX(list_sku, ":", 1) IN (%(site_select)s)
                    ) AS dp
                    INNER JOIN (
                        SELECT
                            list_sku,
                            idlistings_posts
                        FROM
                            listings_posts
                        WHERE 1=1
                            AND list_starter = 1 
                    ) As lp
                         ON lp.list_sku = dp.list_sku 
                    ORDER BY
                        list_date DESC
                    LIMIT %(offset)i, %(limit)i
                    """ % ({'site_select': site_select, 'offset': pg.skipped(), 'limit': pg.entries_per_page()}) 
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
