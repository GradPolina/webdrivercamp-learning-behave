from behave import *
from selenium import webdriver
@step('Navigate to {url}')
def step_impl(context, url):
    context.browser = webdriver.Chrome()
    context.browser.get(url)

