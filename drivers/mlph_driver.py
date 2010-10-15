import mechanize, urllib
import cookielib, re
from pyquery import PyQuery as pq
from dataprocess import crawler, test_crawler

url = 'http://www.mitsulancerph.net/yabb2/YaBB.pl'
br = mechanize.Browser(factory=mechanize.RobustFactory())  
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)
print "entering MLPH site..."
print "logging into site..."
br.open(url)

br.select_form(nr=0)
br['username'] = 'jamongkad'
br['passwrd'] = 'p455w0rd'
br.submit()

print "login in successful!"

html = pq(br.response().read())

processing = True
page = 1

post_content = 'div.message:first'
post_author = 'a[href*="username"]:first'
site = 'MLPH'
regex = 'num=(\d+)'

nxt_pge_cnt = 20
end_pge_cnt = 80

def determine_encode(tex):
    if type(tex) is unicode:
        res = br.find_link(text_regex=tex)
    else:
        res = br.find_link(text=tex)

    return res

while(processing):
    print "Going Car Related posts..."

    if page is 1:
        req = br.click_link(text="Car Related")
        res = br.open(req)
        print "Car Related Url : %s" % (res.geturl())
        print "scraping page 1"
        listings = pq(res.read())
        lists = listings('td.windowbg > div > b > a').map(
            lambda i, e: pq(e).text() if not re.compile('(DISCLAIMER|CHECK THE)').findall(pq(e).text()) else None
        )
        storage_list = [determine_encode(link) for link in lists] 
        crawler(storage_list, mecha_state=br, content=post_content, author=post_author, post_regex=regex, site_id=site, reform_url=False)
        page += 1
        br.back()
       
    else:
        next_page_url = "http://www.mitsulancerph.net/yabb2/YaBB.pl?board=Caritems/%s" % (nxt_pge_cnt)
        print "Page Count at %s" % (nxt_pge_cnt)
        print "scraping page %s" % (next_page_url)
        res_pg_2 = br.open(next_page_url)
        listings = pq(res_pg_2.read()) 
        lists = listings('td.windowbg > div > b > a').map(
            lambda i, e: pq(e).text() if not re.compile('(DISCLAIMER|CHECK THE)').findall(pq(e).text()) else None
        )
        storage_list = [determine_encode(link) for link in lists]   
        crawler(storage_list, mecha_state=br, content=post_content, author=post_author, post_regex=regex, site_id=site, reform_url=False)
        nxt_pge_cnt += 20
        br.back()

        if(nxt_pge_cnt == end_pge_cnt):
            processing = False

