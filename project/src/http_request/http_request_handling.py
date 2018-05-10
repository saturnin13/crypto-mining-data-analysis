import requests
from requests.adapters import HTTPAdapter


class HttpRequestHandling:
    def __init__(self):
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=1)
        self.session.max_redirects = 50
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get_request(self, url):
        try:
            r = self.session.get(url)
            return r.text
        except requests.exceptions.ConnectionError as error:
            print("ERROR: Could not connect to: " + str(url) + ", following error " + str(error))
            return ""


