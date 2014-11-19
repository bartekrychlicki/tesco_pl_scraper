import urllib.parse


class UrlGenerator(object):
    SCHEME = 'http'
    LOCATION = 'ezakupy.tesco.pl'
    CATEGORY_PATH = 'pl-PL/Product/BrowseProducts'

    @classmethod
    def get_homepage(cls):
        return urllib.parse.urlunsplit((
            cls.SCHEME,
            cls.LOCATION,
            '/',
            None,
            None
        ))

    @classmethod
    def make_category_url(cls, category_id, page_no=None):
        params = {'taxonomyId': 'Cat' + category_id}
        if page_no is not None:
            params['pageNo'] = page_no

        params_string = urllib.parse.urlencode(params)
        return urllib.parse.urlunsplit((
            cls.SCHEME,
            cls.LOCATION,
            cls.CATEGORY_PATH,
            params_string,
            None
        ))
