import time
from behave import step
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from behave_basics.components.base import Base

@step('Navigate to {url}')
def step_impl(context, url):
    context.browser.get(url)
@step('Search for {search_item}')
def step_impl(context, search_item):
    base = Base(context.browser)
    search_box_xpath = '//input[@id="search"]'
    search_box = base.find_visible_element(search_box_xpath)
    search_box.clear()
    search_box.send_keys(search_item)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

@step("Gift idea: select {item} from {header}")
def step_impl(context, item, header):
    base = Base(context.browser)
    gift_item_xpath = (f'//div[@data-test="pictureNavigation"]'
                       f'[contains (., "{header}")]'
                       f'//li[contains(., "{item}")]//a')
    item = base.find_visible_element(gift_item_xpath)
    context.browser.execute_script("arguments[0].scrollIntoView();", item)
    item.click()
    time.sleep(5)
