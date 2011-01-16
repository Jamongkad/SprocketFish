import sphinxapi
from db import sql_db as db

class SkuInfo(object):
    def __init__(self):
        self.cl = sphinxapi.SphinxClient()
        self.cl.SetServer("127.0.0.1", 3312)
        self.cl.SetMatchMode(sphinxapi.SPH_MATCH_ALL)
        self.cl.SetSortMode(sphinxapi.SPH_SORT_RELEVANCE)
 
    def sku_info(self, ids, search_term):

        sql = """
            SELECT 
                SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) AS post_id
              , data_prep.list_title AS title
              , listings_posts.idlistings_posts AS list_id
              , data_prep.list_sku AS sku
              , listings_posts.list_text_text AS text
              , listings_posts.list_text_html AS html
              , listings_posts.list_author AS auth
              , data_prep.list_url AS url
            FROM 
                data_prep 
            INNER JOIN
                listings_posts
                ON data_prep.list_sku = listings_posts.list_sku
            WHERE 1=1 
                AND SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) IN (%(ids)s) 
                AND listings_posts.list_starter = 1 
            GROUP BY
                data_prep.list_title
            ORDER BY
                data_prep.list_date DESC
            """ % ({'ids': ids})

        rp = db.bind.execute(sql)

        entry_object = {}
        storage = []
        for entry in rp.fetchall():
            docs = []
            docs.append(unicode(entry[4], errors="ignore"))
            entry_object = {
                'post_id' : entry[0], 
                'title' : entry[1],
                'list_id' : entry[2], 
                'sku' : entry[3],
                'url' : entry[7],
                'excerpts' : self.cl.BuildExcerpts(docs, 'posts', search_term, { 'single_passage' : True })
            }

            storage.append(entry_object)

        return storage
