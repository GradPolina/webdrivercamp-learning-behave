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
    item_xpath = (f'//div[@data-test="pictureNavigation"]'
                  f'[contains (., "{header}")]'
                  f'//li[contains(., "{item}")]//a')
    base = Base(context.browser)
    item = base.find_visible_element(item_xpath)
    context.browser.execute_script("arguments[0].scrollIntoView();", item)
    item.click()
    time.sleep(10)

@step("Verify all prices < {condition}")
def step_impl(context, condition):
    prices_xpath = (f'//div[@data-test="@web/ProductCard/ProductCardVariantDefault"]'
                    f'//span[@data-test="current-price"]')
    titles_xpath = (f'//div[@data-test="@web/ProductCard/ProductCardVariantDefault"]'
                    f'//a[@data-test="product-title"]')

    results_price = Base(context.browser).find_all_elements(prices_xpath)
    results_title = Base(context.browser).find_all_elements(titles_xpath)

    all_prices = [float(price.text.replace("$", "").split()[-1]) for price in results_price]
    all_titles = [title.text for title in results_title]

    mismatch = {}
    for price, title in zip(all_prices, all_titles):
        if condition == "<":
            condition, exp_price = condition.strit().split()
            if float(price) >= float(exp_price):
                mismatch[title] = price

    if mismatch:
        for title, price in mismatch.items():
            price(f'Item {title} has a price of {price}')
        raise AssertionError("Some items have prices greater than the expected value.")







