from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
KEYWORD = 'ipad'

def index_Page(page):
    print("page:",page)
    try:
        url = 'https://s.taobao.com/search?q='+quote(KEYWORD)
        browser.get(url)
        if page>1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input'))
            )
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-page div.form > span.btn.J_Submit'))
            )
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page))
        )
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_Page(page)

def get_products():
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('deal-cnt').text()
        }
    print(product)


MAX_PAGE = 100
def main():
    for i in range(1,MAX_PAGE+1):
        index_Page(i)

main()

