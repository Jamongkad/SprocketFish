from dataprocess import crawler, test_crawler
import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq

#url = 'http://z11.invisionfree.com/JDM_Underground'
#url = 'http://s3.zetaboards.com/HCP/site/'
#url = "http://grupotoyota.com.ph/board/"
url = 'http://www.mitsulancerph.net/yabb2/YaBB.pl'
br = mechanize.Browser(factory=mechanize.RobustFactory())  
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)
print "logging into site..."
br.open(url)
br.select_form(nr=0) 
br['username'] = 'jamongkad'
br['passwrd'] = 'p455w0rd'
br.submit()

#req = br.click_link(text='Underground Parts')
#res = br.open(req)
#print "Underground Parts Url : %s" % (res.geturl()) 
#print "scraping page 1"
#listings = pq(res.read())
#lists = listings('td.darkrow1').eq(5).parents('tr').siblings('tr').children('td > a[href*="showtopic"]').not_('.linkthru')
#storage_list = lists.map(lambda i, e: br.find_link(text=pq(e).text().replace("  ", " ")))

#print "going to Parts & Accessories"
#req = br.click_link(text='Parts & Accessories')
#res = br.open(req)

html = pq(br.response().read())

#(selling_link, ) = html('a[href*="./viewforum.php?f=8"]').map(lambda i, e: pq(e).attr('href'))
#req = br.find_link(url=selling_link)
#res = br.open(req)

#print "scraping page 1"
#listings = pq(res.read())
#storage_list = listings('td.row1 > img[src*="topic"]').parents('td.row1').siblings('td.row1 > a.topictitle').\
#                     map(lambda i, e: br.find_link(url=pq(e).attr('href')))

req = br.click_link(text="Car Related")
res = br.open(req)
listings = pq(res.read())

def follow_linky(num=0):
    br.follow_link(storage_list[num])
    post = pq(br.response().read())
    return post
