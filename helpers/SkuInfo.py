import sphinxapi
from db import sql_db, text

class SkuInfo(object):
 
    def sku_info(self, ids, search_term, sc):

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
              , data_prep.list_date AS date
            FROM 
                data_prep 
            INNER JOIN
                listings_posts
                ON data_prep.list_sku = listings_posts.list_sku
            WHERE 1=1 
                AND SUBSTRING_INDEX( SUBSTRING_INDEX(listings_posts.idlistings_posts, ':', 2), ':', -1) IN (':x')
                AND listings_posts.list_starter = 1 
                AND YEAR(data_prep.list_date) <= YEAR(NOW())
                AND YEAR(data_prep.list_date) >= YEAR(NOW()) - 1
            ORDER BY
                data_prep.list_date DESC
            """ 
        rp = sql_db.execute(sql, params=dict(x=ids)).fetchall()
        return rp, ids

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
                'date': entry[8],
                'excerpts' : sc.BuildExcerpts(docs, 'posts', search_term, { 'single_passage' : True }) if search_term else ""
            }

            storage.append(entry_object)

        return storage
