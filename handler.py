import os
import json
import yaml
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from notify import notify, WebDiff


class Web:
    def __init__(self, options, path='./chromedriver/chromedriver', screen_shot_path='./'):
        self._driver = webdriver.Chrome(path, chrome_options=options)
        self.screen_shot_count = 0
        self.screen_shot_path = screen_shot_path

    def get_screen_shot(self, element_id=None):
        if element_id is not None:
            ActionChains(self._driver).move_to_element(self._driver.find_element_by_id(element_id)).perform()
            self._driver.save_screenshot('{}/{}.png'.format(self.screen_shot_path, self.screen_shot_count))
        else:
            self._driver.save_screenshot('{}/{}.png'.format(self.screen_shot_path, self.screen_shot_count))
        print('screenshot {} saved!'.format(self.screen_shot_count))
        self.screen_shot_count += 1
        return self

    def save_page_source(self):
        with open("{}.html".format(self._driver.title), 'w') as f:
            f.write(self._driver.page_source)
        return self

    def get_page_source(self):
        return self._driver.page_source

    def find_element_by_id(self, id_):
        return self._driver.find_element_by_id(id_)

    def find_element_by_xpath(self, xpath):
        return self._driver.find_element_by_xpath(xpath)

    def print_page(self):
        print(self._driver.page_source)

    def go_to(self, url):
        self._driver.get(url)
        return self

def differ(event, context):
    options = Options()
    options.binary_location = './chromedriver/headless-chromium'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
    web = Web(options)

    with open('config.yml', 'r') as c:
        config = yaml.safe_load(c)

    results = []
    for w in config['websites']:
        for k, v in w.items():
            try:
                current = web.go_to(v['url']).find_element_by_xpath(v['xpath']).get_attribute('innerHTML')
            except Exception as e:
                # TODO: handling element not found instead general exception
                print(e)
                current = None
            diff = WebDiff(title=k, url=v['url'], original=v.get('original', None), current=current)
            if diff.original != diff.current:
                # Log page source to debug what's the difference.
                results.append(diff)

    if len(results):
        notify(results)

    return {"results": [r._asdict() for r in results]}

if __name__ == '__main__':
    differ('', '')
