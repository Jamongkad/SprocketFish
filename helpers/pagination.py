
class Pagination(object):
    def __init__(self, per_page, total_rows, urls):
        self.per_page   = per_page
        self.total_rows = total_rows
        self.urls = urls

    def buildLinks(self):
        return dict([(i + 1, ("%s/%d" % (self.urls, i * self.per_page))) 
                      for i in range(0, self.total_rows+1) 
                          if i * self.per_page <= self.total_rows])
