from dataprocess import crawler
import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq
from PageData import PageData
from log_writer import log_message

def main():
    url = 'http://s3.zetaboards.com/HCP/site/'
    br = mechanize.Browser(factory=mechanize.RobustFactory())  
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)
    print "entering hcp site..."
    print "logging into site..."
    br.open(url)

    br.select_form(nr=0)
    br['uname'] = 'jamongkad'
    br['pw'] = 'password'
    br.submit()

    processing = True

    post_content = 'td.c_post'
    post_author = 'td.c_username'
    site_id = 'HCP'
    regex = 'HCP\/topic\/(\d+)/'

    orig_post_date = 'span.left'
    edited_post_date = 'div.editby'
    date_regex = '([A-Za-z]{3}\s[0-9]{1,2}\s[0-9]{4})'

    nxt_pge_cnt = 2
    end_pge_cnt = 5
    page = 1

    while(processing):
        print "going to Parts & Accessories" 
        if page is 1:
            req = br.click_link(text='Parts & Accessories')
            res = br.open(req)
            print "scraping page 1"
            listings = pq(res.read())
            storage_list = listings('td.c_cat-title > a[href*="topic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))
            
            pd = PageData(storage_list, br)\
                     .add_content(post_content, post_author, regex)\
                     .post_date(orig_post_date, edited_post_date, date_regex)\
                     .with_site_id(site_id).if_reform_url(False)
 
            crawler(pd)

            page += 1
            log_message('hcp-driver_%d' % (page)) 
            br.back()
        else:
            next_page_url = "http://s3.zetaboards.com/HCP/forum/21305/%s" % (nxt_pge_cnt)
            print "scraping page %s" % (next_page_url)
            res_pg_2 = br.open(next_page_url)
            listings = pq(res_pg_2.read())
            storage_list = listings('td.c_cat-title > a[href*="topic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))

            pd = PageData(storage_list, br)\
                     .add_content(post_content, post_author, regex)\
                     .post_date(orig_post_date, edited_post_date, date_regex)\
                     .with_site_id(site_id).if_reform_url(False)
             
            crawler(pd)
            nxt_pge_cnt += 1

            log_message('hcp-driver_%d' % (nxt_pge_cnt)) 
            br.back()
            
            if(nxt_pge_cnt == end_pge_cnt):
                processing = False
