
class Pagination(object):
    def __init__(self, per_page, total_rows, urls):
        self.per_page   = per_page
        self.total_rows = total_rows
        self.urls = urls

    def paginate(self):
        return dict([(Pages(i).showPages(), 
                      Links(self.urls, i * self.per_page).showLinks()) 
                      for i in range(0, self.total_rows+1) 
                          if i * self.per_page <= self.total_rows])


class Links(object):
    def __init__(self, urls, per_page):
        self.urls     = urls
        self.per_page = per_page  

    def showLinks(self):
        return "%s/%d" % (self.urls, self.per_page)

class Pages(object):
    def __init__(self, pages):
        self.pages    = pages
        self.page_num = 1

    def showPages(self):
        return self.pages + self.page_num

class PaginationResultObject(object):
    pass
