import time
from behave import step
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from behave_basics.components.base import Base

@step('Navigate to {url}')
def step_impl(context, url):
    context.browser.get(url)
    context.execute_steps('Then Print the current url')


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
    header_xpath = '//h1/span[contains(., "iphone")]'
    result_header = base.find_element(header_xpath)
    header_text = context.browser.execute_script('return arguments[0].innerText', result_header)
    assert search_item.lower() in header_text.lower(), f"Header doesn't contain '{search_item}': {header_text}"


@step("Collect all items on the first page into {var}")
@step("Collect all items on the first page into {var} on the {level} level")
def step_impl(context, var, level=None):
    prices_xpath = (f'//div[@data-test="@web/ProductCard/ProductCardVariantDefault"]'
                    f'//span[@data-test="current-price"]')
    items_xpath = (f'//div[@data-test="@web/ProductCard/ProductCardVariantDefault"]'
                   f'//a[@data-test="product-title"]')
    shipping_xpath = (f'//div[@data-test="@web/ProductCard/ProductCardVariantDefault"]'
                      f'//span[contains(text(), "Ships free")]')

    results_price = Base(context.browser).find_all_elements(prices_xpath)
    results_items = Base(context.browser).find_all_elements(items_xpath)
    results_shipping = Base(context.browser).find_all_elements(shipping_xpath)

    collected_items = []

    all_prices = [float(price.text.replace("$", "").split()[-1]) for price in results_price]
    all_items = [item.text for item in results_items]
    all_shipping = [shipping.text for shipping in results_shipping]

    for price, item, shipping in zip(all_items, all_prices, all_shipping):
        collected_items.append({'title': item, 'price': price, 'shipping': shipping})
    if level == 'feature':
        setattr(context.feature, var, collected_items)
    else:
        setattr(context, var, collected_items)


@step("Verify all collected results' {param} is {condition}")
def step_impl(context, param, condition):
    collected_items = context.feature.collected_items
    if param == 'price':
        mismatch = {}
        for item in collected_items:
            value = item['price']
            if condition == "<":
                condition, exp_price = condition.strit().split()
                if float(value) >= float(exp_price):
                    mismatch[item['title']] = value

        if mismatch:
            for title, value in mismatch.items():
                print(f'Item {title} has a price of {value}')
                raise AssertionError("Some items have prices greater than the expected value.")

    elif param == 'shipping':
        mismatch = {}
        for item in collected_items:
            if item['shipping'] != condition:
                mismatch[item['title']] = item['shipping']
        if mismatch:
            for title, shipping in mismatch.items():
                print(f'Item {title} has a price of {shipping}')
                raise AssertionError("Some items do not have the expected shipment condition.")


@step('Print the current url')
def step_impl(context):
    current_url = context.browser.current_url
    print(f"Current URL: {current_url}")


