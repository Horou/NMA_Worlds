import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class WebParser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )
        self.driver.maximize_window()

    def wait(self, css_selector):
        _, first_element = next(iter(css_selector.items()))
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, first_element)))

    def parse(self, url, xpath_selector: dict) -> dict:
        try:
            self.driver.get(url)
            self.wait(xpath_selector)
            time.sleep(10)
            return {
                key: self.driver.find_element(By.XPATH, value)
                for key, value in xpath_selector.items()
            }
        except Exception as e:
            print(e)
            return {}
        finally:
            self.close()

    def close(self):
        self.driver.close()
        self.driver.quit()

test = WebParser()
url_test = "https://www.asurascans.com/0906168628-my-daughter-is-a-dragon-chapter-25/"
css_selector_test = {
    "0": '//div[@class="readerarea"]',
    "1": '//div[@class="readerarea"]//span[@itemprop="author"]/text()',
    "2": '//div[@id="readerarea"]//p//img/@src'
}
test2 = test.parse(url_test, css_selector_test)
pprint(test2)

