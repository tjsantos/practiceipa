import os
import hashlib
import json
import requests
from requests.utils import default_user_agent
from requests.exceptions import RequestException
import time

class WikimediaDownloader:
    default_delay = 0.1 # seconds to wait between each request

    def __init__(self):
        # supply intent and contact info in user-agent
        website = 'https://github.com/tjsantos/practiceipa'
        user_agent_add = '( wiktionary pronunciations download; {} )'.format(website)
        self.headers = {'User-Agent': default_user_agent() + ' ' + user_agent_add}

        self.last_request_time = time.time()
        self.delay = self.default_delay

    def download(self, filename):
        '''Given a wikimedia filename, download and return the content as bytes. Buffer subsequent
        requests using exponential backoff.'''
        wait_time = self.delay - (time.time() - self.last_request_time)
        wait_time = max(wait_time, 0)
        time.sleep(wait_time)
        try:
            # request the file from the server
            md5 = hashlib.md5(filename.encode()).hexdigest()
            url = "http://upload.wikimedia.org/wikipedia/commons/{}/{}/{}".format(
                md5[:1], md5[:2], filename
            )
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                raise AssertionError(
                    'file: {}, status code: {}'.format(filename, response.status_code)
                )
        except (AssertionError, RequestException) as e:
            print(time.strftime('%H:%M:%S'), e)
            self.delay *= 2
        else:
            self.delay = self.default_delay
        finally:
            self.last_request_time = time.time()

        if self.delay > self.default_delay:
            print('will buffer {} seconds before next request'.format(delay))
        return response.content
