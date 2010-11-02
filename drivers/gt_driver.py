import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq
from dataprocess import crawler
from PageData import PageData
from log_writer import log_message

url = "http://grupotoyota.com.ph/board/"
br = mechanize.Browser(factory=mechanize.RobustFactory())  
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)
print "entering GT site..."
print "logging into site..."
br.open(url)

br.select_form(nr=0)
br['username'] = 'jamongkad'
br['password'] = 'p455w0rd'
br.submit()

print "login in successful!"
html = pq(br.response().read())
processing = True

post_content = 'div.postbody'
post_author = 'b.postauthor'
site_id = 'GT'
regex = '\&t=(\d+)'

orig_post_date = 'td.gensmall > div:nth-child(2)'
edited_post_date = None
date_regex = '([A-Za-z]{3}\s[0-9,]{1,2}[,]\s[0-9]{4})'

page = 1
nxt_pge_cnt = 25
end_pge_cnt = 150

while(processing):
    print "going to Auto parts Selling..."

    if page is 1:
        (selling_link ,)= html('a[href*="./viewforum.php?f=8"]').map(lambda i, e: pq(e).attr('href')) 
        req = br.find_link(url=selling_link)
        res = br.follow_link(req)
        
        print "Auto Parts - Selling (Car Stuff, Parts, Accessories)... Url: %s" % (res.geturl())
        print "scraping page 1"
        listings_html = pq(res.read())
        storage_list = listings_html('td.row1 > img[src*="topic"]').parents('td.row1').siblings('td.row1 > a.topictitle').\
                       map(lambda i, e: br.find_link(url=pq(e).attr('href')))

        pd = PageData(storage_list, br)\
                 .add_content(post_content, post_author, regex)\
                 .post_date(orig_post_date, edited_post_date, date_regex)\
                 .with_site_id(site_id).if_reform_url(True)

        crawler(pd)
        page += 1
        #log_message('gt-driver_%d' % (page)) 
        br.back()
    else:
        next_page_url = "http://grupotoyota.com.ph/board/viewforum.php?f=8&start=%s" % (nxt_pge_cnt)
        print "scraping page %s" % (next_page_url)
        print "Page Count at %s" % (nxt_pge_cnt)
        res_pg_2 = br.open(next_page_url)
        listings_2 = pq(res_pg_2.read())
        storage_list = listings_2('td.row1 > img[src*="topic"]').parents('td.row1').siblings('td.row1 > a.topictitle').\
                     map(lambda i, e: br.find_link(url=pq(e).attr('href'))) 

        pd = PageData(storage_list, br)\
                 .add_content(post_content, post_author, regex)\
                 .post_date(orig_post_date, edited_post_date, date_regex)\
                 .with_site_id(site_id).if_reform_url(True)

        crawler(pd)
        nxt_pge_cnt += 25

        if(nxt_pge_cnt == end_pge_cnt):
            processing = False

        #log_message('gt-driver_%d' % nxt_pge_cnt) 
        br.back() 
