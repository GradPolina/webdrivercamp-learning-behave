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

@step("Select {option} in {section}")
def step_impl(context, option, section):
    option_xpath = (f'//div[@data-test="pictureNavigation"]'
                    f'[contains (., "{section}")]'
                    f'//li[contains(., "{option}")]//a')
    base = Base(context.browser)
    option = base.find_visible_element(option_xpath)
    context.browser.execute_script("arguments[0].scrollIntoView();", option)
    option.click()
    time.sleep(10)

@step("Verify header of the page contains {search_item}")
def step_impl(context, search_item):
    base = Base(context.browser)
    header_xpath = '//h1'
    result_header = base.find_visible_element(header_xpath)
    header_text = result_header.text
    assert search_item.lower() in header_text.lower(), f"Header doesn't contain '{search_item}': {header_text}"

@step("Collect all items on the first page into {context_var}")
def step_impl(context, context_var):
    prices_xpath = (f'//div[@data-test="@web/ProductCard/ProductCardVariantDefault"]'
                    f'//span[@data-test="current-price"]')
    items_xpath = (f'//div[@data-test="@web/ProductCard/ProductCardVariantDefault"]'
                   f'//a[@data-test="product-title"]')

    results_price = Base(context.browser).find_all_elements(prices_xpath)
    results_items = Base(context.browser).find_all_elements(items_xpath)

    collected_items = []

    all_prices = [float(price.text.replace("$", "").split()[-1]) for price in results_price]
    all_items = [item.text for item in results_items]

    for price, item in zip(all_items, all_prices):
        collected_items.append({'title': item, 'price': price})
    setattr(context, context_var, collected_items)

@step("Verify all collected results' prices is {condition}")
def step_impl(context, condition):
    collected_items = context.collected_items
    mismatch = {}
    for item in collected_items:
        price = item['price']
        if condition == "<":
            condition, exp_price = condition.strit().split()
            if float(price) >= float(exp_price):
                mismatch[item['title']] = price

    if mismatch:
        for item, price in mismatch.items():
            price(f'Item {item} has a price of {price}')
            raise AssertionError("Some items have prices greater than the expected value.")


