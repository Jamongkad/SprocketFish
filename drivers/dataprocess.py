from sqlalchemy.ext.sqlsoup import SqlSoup

import mechanize, urllib
import cookielib, re, sys, os
from pyquery import PyQuery as pq
import MultiDict
from dateutil import parser
from datetime import date, timedelta

#try: 
#    sql_db = SqlSoup('mysql://root:p455w0rd@localhost/hero_fish_db?charset=utf8&use_unicode=0', echo=True)
#except:
#    sql_db.rollback()
#    raise

sql_db = SqlSoup('mysql://root:p455w0rd@localhost/hero_fish_db?charset=utf8&use_unicode=0')

def crawler(pd):
     
    storage_list = fine_tune_urls(pd.storage_list, pd.post_regex)

    site_id = sql_db.site.filter(sql_db.site.site_nm==pd.site_id).first()
    br = pd.mecha_state

    print "processing list views..."
    for links in storage_list:
        br.follow_link(links)
        d = pq(br.response().read()) 
        posts = d(pd.content).map(lambda i, e: (pq(e).text(), pq(e).html()))
        authors = d(pd.author).map(lambda i ,e: pq(e).text())
        
        if hasattr(pd, 'create_date'):
            get_date = d(pd.create_date).text()

        if hasattr(links, 'post_date'):
            get_date = links.post_date

        if hasattr(pd, 'edit_date'):
            get_edit_date = d(pd.edit_date).text()

        if get_date: 
            c_date = re.compile(pd.date_regex).findall(get_date)

        if get_edit_date:
            e_date = re.compile(pd.date_regex).findall(get_edit_date) 

        linky = links.text

        l_title = unicode(linky, 'latin-1').encode('utf-8')

        (matches, ) = re.compile(pd.post_regex).findall(links.url)
        url = define_link(links, pd.reform_url)

        rawfromiso = authors[0].encode('iso-8859-1')
        l_author = unicode(rawfromiso, 'iso-8859-1').encode('utf-8')
        #debug output
        print "-------------------------------------------------"
        if matches:
            sku = "%s:%s" % (pd.site_id, matches)
            print "sku: %s" % (sku)
        import chardet
        print "scraping entry: %s, url: %s, author: %s" % (l_title, url, l_author)
        if get_date:
            print "created on %s" % (c_date)
        if get_edit_date:
            print "edited on %s" % (e_date)
  
        #database stuff
        try:
            date = current_date(get_date, get_edit_date, pd.date_regex, pd.site_id)
            print "extracting post id for sku..."
            if matches:
                print "extraction successful!!"
                sku = "%s:%s" % (pd.site_id, matches)
                print "checking record for existing sku..."
                my_list = sql_db.data_prep.filter(sql_db.data_prep.list_sku==sku).first()
                print "finalized date on : %s" % (date)
            else:
                print "failure in sku extraction..."
                sys.exit()   

            pdp = ProcessDataPosts(posts, authors, pd.site_id, date)
            check_update_post(my_list, site_id, url, sku, l_title, pdp)

        except Exception, err:
            print "something went wrong! rolling back table! ERROR: %s" % (str(err))
            sql_db.rollback()
            sys.exit()

        br.back()
    
def check_update_post(my_list, site_id, url, sku, l_title, data_obj):

    post_data = data_obj.process_post_data()
    thread_author = data_obj.thread_author
    post_date = data_obj.post_date

    if my_list:
        print "sku record db exists!"
        title = my_list.list_title

        print "checking for new title..." 
        if title != l_title:
            print "title has been updated! updating now..."
            my_list.list_title = l_title

        print "checking for updated post..."
        for author in post_data.keys():
            for idx, p in enumerate(post_data.getall(author)): 
                post_id = "postid-%s" % (idx)
                post_id_sku = "%s:%s:%s" % (sku, post_id, author)  

                existing_post = sql_db.listings_posts.filter(sql_db.listings_posts.idlistings_posts==post_id_sku).first()

                pst_text = p[0].encode('utf-8')
                pst_html = p[1].encode('utf-8')

                if existing_post:
                    if pst_text != existing_post.list_text_text and pst_html != existing_post.list_text_html:
                        existing_post.list_text_text = pst_text
                        existing_post.list_text_html = pst_html
                else: 
                    print "inserting posts %s" % (post_id)
                    sql_db.listings_posts.insert(idlistings_posts=post_id_sku, list_sku=sku, 
                                                 list_text_text=pst_text, list_text_html=pst_html, list_author=author)

        existing_main_post = sql_db.data_prep.filter(sql_db.data_prep.list_sku==sku).first()

        if existing_main_post.list_date == " " or existing_main_post.list_date != post_date:
            existing_main_post.list_date = post_date

        sql_db.commit()

    else:
        print "new sku! inserting into data preparation table."
        #insert post
        sql_db.data_prep.insert(list_sku=sku, list_title=l_title, site_id=site_id.site_id, list_url=url, list_authr=thread_author, list_date=post_date)
        #insert sub posts and authors
        for author in post_data.keys():
            for idx, p in enumerate(post_data.getall(author)): 
                post_id = "postid-%s" % (idx)
                post_id_sku = "%s:%s:%s" % (sku, post_id, author)   
                list_starter_check = is_list_starter(post_id, thread_author, author)
                
                print "inserting post %s" % (post_id_sku) 
                sql_db.listings_posts.insert(idlistings_posts=post_id_sku, list_sku=sku, 
                                             list_text_text=p[0], list_text_html=p[1], list_author=author, list_starter=list_starter_check)
        
        sql_db.commit()
        print "insertion successful!"

def is_list_starter(post_id, thread_author, author): 
    check = 0
    if post_id == "postid-0" and thread_author == author:
        check = 1

    return check

def define_link(links, reform_url_flag): 
    if reform_url_flag: 
        link_url = links.url
        reformed_url = link_url.split('./')[1]
        url = "http://grupotoyota.com.ph/board/%s" % (reformed_url)
    else:
        url = links.url

    return url

def find_quote(text):
    match = re.compile('QuoteBegin').findall(text)
    return match

class ProcessDataPosts(object):
    def __init__(self, posts, authors, site_id, post_date):
        self.posts   = posts
        self.authors = authors
        self.site_id = site_id
        self.thread_author = self._process_author(authors[0])
        self.post_date = post_date

    def _process_author(self, author):
        rawfromiso = author.encode('iso-8859-1')
        return unicode(rawfromiso, 'iso-8859-1').encode('utf-8')

    def process_post_data(self):
        storage = MultiDict.OrderedMultiDict()
        if self.site_id == 'JDMU': 
            clean_posts = [(post[0], post[1]) for post in self.posts if not find_quote(post[0])]
        else:
            clean_posts = [(post[0], post[1]) for post in self.posts]
 
        for i in range(0, len(self.authors)):
            storage[self.authors[i]] = clean_posts[i]

        return storage

def fine_tune_urls(storage_list, regex):
    return [i for i in storage_list if re.compile(regex).findall(i.url)]

def current_date(get_date, get_edit_date, date_regex, site_id):

    if get_date and get_edit_date is None:
        post_date = re.compile(date_regex).findall(get_date) 

    if get_edit_date:
        post_date = re.compile(date_regex).findall(get_edit_date) 
    
    if site_id is 'MLPH':
        if get_date == 'Today' or get_edit_date == 'Today':
            return date.today().isoformat()
        
        if get_date == 'Yesterday' or get_edit_date == 'Yesterday':
            yesterday = date.today() - timedelta(1)
            return yesterday.isoformat()

        post_date = re.compile(date_regex).findall(get_date) 

    return parser.parse(post_date[0]).date().isoformat()
