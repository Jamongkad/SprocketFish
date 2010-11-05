import sphinxapi
from db import sql_db as db

class SkuInfo(object):
    def __init__(self):
        self.cl = sphinxapi.SphinxClient()
        self.cl.SetServer("127.0.0.1", 3312)
        self.cl.SetMatchMode(sphinxapi.SPH_MATCH_ALL)
        self.cl.SetSortMode(sphinxapi.SPH_SORT_RELEVANCE)
 
    def sku_info(self, post_id, search_term):

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
        docs = []
        for entry in rp.fetchall():
            docs.append(unicode(entry[4], errors="ignore"))
            storage = {
                'post_id' : entry[0], 
                'title' : entry[1],
                'list_id' : entry[2], 
                'sku' : entry[3],
                'excerpts' : self.cl.BuildExcerpts(docs, 'posts', search_term, { 'single_passage' : True })
            }

        return storage
