from dataprocess import crawler
import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq
from PageData import PageData

def main():
    url = 'http://z11.invisionfree.com/JDM_Underground'
    br = mechanize.Browser(factory=mechanize.RobustFactory())  
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)
    print "entering jdmu site..."
    print "logging into site..."
    br.open(url)

    br.select_form(nr=0) 
    br['UserName'] = 'jamongkad'
    br['PassWord'] = 'p455w0rd'
    br.submit()

    processing = True
    page = 1

    post_content = 'div.postcolor'
    post_author = 'span.normalname a span'

    orig_post_date = 'span.postdetails:first'
    edited_post_date = 'span.edit:first'
    date_regex = '([A-Za-z]{3}\s[0-9]{1,2}\s[0-9]{4})'

    site_id = 'JDMU'
    regex = 'index.php\?showtopic=(\d+)'

    nxt_pge_cnt = 40
    end_pge_cnt = 120

    while(processing):
        print "going to Underground Parts"
         
        if page is 1: 
            req = br.click_link(text='Underground Parts')
            res = br.open(req)
            print "Underground Parts Url : %s" % (res.geturl()) 
            print "scraping page 1"
            listings = pq(res.read())
            #lists = listings('td.darkrow1').eq(5).parents('tr').siblings('tr').children('td > a[href*="showtopic"]').not_('.linkthru')
            #storage_list = lists.map(lambda i, e: pq(e).attr('href'))
            print listings('td.darkrow1').text()
            """  
            pd = PageData(storage_list, br)\
                     .add_content(post_content, post_author, regex)\
                     .post_date(orig_post_date, edited_post_date, date_regex)\
                     .with_site_id(site_id).if_reform_url(False)
            crawler(pd) 
            """ 
            page += 1
            br.back()
        else:
            next_page_url = "http://z11.invisionfree.com/JDM_Underground/index.php?showforum=3&prune_day=100&sort_by=Z-A&sort_key=last_post&st=%s" % (nxt_pge_cnt)
            print "Page Count at %s" % (nxt_pge_cnt)
            print "scraping page %s" % (next_page_url)
            res_pg_2 = br.open(next_page_url)
            listings_2 = pq(res_pg_2.read())
            storage_list_2 = listings_2('td.row4 > a[href*="showtopic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href')))
            print storage_list_2
            """
            pd = PageData(storage_list_2, br)\
                     .add_content(post_content, post_author, regex)\
                     .post_date(orig_post_date, edited_post_date, date_regex)\
                     .with_site_id(site_id).if_reform_url(False)
            crawler(pd)
            """ 
            nxt_pge_cnt += 40
            br.back()

            if(nxt_pge_cnt == end_pge_cnt):
                processing = False
