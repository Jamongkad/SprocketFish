class PageData(object):

    def __init__(self, storage_list, mecha_state):
        self.storage_list = storage_list
        self.mecha_state = mecha_state
        self.content = None
        self.author = None
        self.create_date = None
        self.edit_date = None
        self.date_regex = None
        self.post_regex = None
        self.site_id = None
        self.reform_url = False

    def add_content(self, content, author, post_regex):
        self.content = content
        self.author = author
        self.post_regex = post_regex
        return self

    def post_date(self, create_date, edit_date, date_regex):
        self.create_date = create_date
        self.edit_date = edit_date
        self.date_regex = date_regex
        return self

    def with_site_id(self, site_id):
        self.site_id = site_id
        return self

    def if_reform_url(self, reform_url):
        self.reform_url = reform_url
        return self

