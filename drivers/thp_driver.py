import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq
from dataprocess import process_list_view

url = "http://z7.invisionfree.com/teamhondaphilippines/index.php?"
br = mechanize.Browser(factory=mechanize.RobustFactory())  
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)
print "entering thp site..."
print "logging into site..."
br.open(url)
br.select_form(nr=0)
br['UserName'] = 'jamongkad'
br['PassWord'] = 'p455w0rd'
br.submit()
print "login successful!"

processing = True
page = 1
while(processing):
    print "going to Parts&Accessories"
    req = br.click_link(text='Parts&Accessories')
    res = br.open(req)
    if page is 1:
        print "scraping page 1"
        listings = pq(res.read())
        lists = listings('td.darkrow1').eq(5).parents('tr').siblings('tr').children('td > a[href*="showtopic"]').not_('.linkthru')
        storage_list = lists.map(lambda i, e: br.find_link(url=pq(e).attr('href')))
        process_list_view(storage_list, br, pq, 'td.post2 > div.postcolor', 3)
        page = 2
        br.back()
    else:
        print "scraping page 2"
        req_pg_2 = br.find_link(text='2')
        res_pg_2 = br.follow_link(req_pg_2)
        listings_2 = pq(res_pg_2.read())
        storage_list = listings_2('td.row4 > a[href*="showtopic"]').map(lambda i, e: br.find_link(url=pq(e).attr('href'))) 
        process_list_view(storage_list, br, pq, 'td.post2 > div.postcolor', 3)
        processing = False
