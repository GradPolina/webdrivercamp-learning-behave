from selenium import webdriver

def before_all(context):
    context.browser = webdriver.Chrome()
    context.browser.implicitly_wait(10)
def after_all(context):
    context.browser.quit()