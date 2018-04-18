import requests

class HttpRequestHandling:
    def __init__(self):
        pass

    def get_request(self, url):
        r = requests.get(url)
        return r.text


