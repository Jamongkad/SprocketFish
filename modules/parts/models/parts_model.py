import app_globals

from db import sql_db as db, text

class Sites(object):
    def show_sites(self, with_quotes=True):
        sql = """SELECT site_nm FROM site"""
        req = db.bind.execute(sql)
        if with_quotes:
            return ["'" + site.site_nm + "'" for site in req.fetchall()] 
        return [site.site_nm for site in req.fetchall()] 

    def view_entry(self, list_id):
        sql = text("""
            SELECT   
                data_prep.list_title AS title
              , listings_posts.list_text_html AS html
              , listings_posts.list_author AS auth
              , DATE_FORMAT(data_prep.list_date, GET_FORMAT(DATE, 'USA')) AS date
              , data_prep.list_url AS url
            FROM 
                data_prep
            INNER JOIN
                listings_posts
                ON data_prep.list_sku = listings_posts.list_sku
            where 1=1 
                AND data_prep.list_sku = :x
                AND listings_posts.list_starter = 1 
        """) 
        rp = db.bind.execute(sql, x=list_id)

        return rp
