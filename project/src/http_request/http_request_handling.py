import requests
from requests.adapters import HTTPAdapter


class HttpRequestHandling:
    def __init__(self):
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=6)
        self.session.max_redirects = 50
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get_request(self, url):
        r = self.session.get(url)
        return r.text


