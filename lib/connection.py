import urllib.request
import urllib.parse


class Connector(object):
    USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, '
                  'like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0'
                  '.1025.168 Safari/535.19')
    ACCEPT = ('text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/webp,*/*;q=0.8')
    HEADERS = {
        'User-Agent': USER_AGENT,
        'Accept': ACCEPT
    }

    @classmethod
    def create_request(cls, url):
        request = urllib.request.Request(url, headers=cls.HEADERS)
        return urllib.request.urlopen(request)

    @classmethod
    def read_url(cls, url):
        return cls.create_request(url).read().decode('utf-8')


class UrlMaker(object):
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
