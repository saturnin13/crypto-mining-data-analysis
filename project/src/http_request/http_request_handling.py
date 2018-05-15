import requests
import urllib3
from requests.adapters import HTTPAdapter


class HttpRequestHandling:
    def __init__(self):
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=6)
        self.session.max_redirects = 50
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_request(self, url, verify=True):
        try:
            if(not verify):
                print("WARNING: Connecting without TLS verifiation: " + str(url) + ", potential MITM attack possible")
            r = self.session.get(url, verify=verify)
            return r.text
        except requests.exceptions.ConnectionError as error:
            print("ERROR: Could not connect to: " + str(url) + ", following error " + str(error))
            return ""


