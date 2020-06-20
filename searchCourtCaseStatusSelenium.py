"""
Automate filling of the forms on eCourts India website
"""
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


import lxml.html
import urllib.request as urllib2
import pprint
import http.cookiejar as cookielib

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')

config = configparser.ConfigParser()
config.read('./config.txt')
website_url = config['config1']['url']

# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get(str(website_url))

# court_establishment = driver.find_element_by_id("radCourtEst")
# court_establishment.click()

# select_court_code = Select(driver.find_element_by_id('court_code'))
# select_court_code.select_by_value(config['config1']['court_code'])

# select_case_type = Select(driver.find_element_by_id('case_type'))
# select_case_type.select_by_value(config['config1']['case_type'])

# search_case_no = driver.find_element_by_id("search_case_no")
# search_case_no.send_keys(config['config1']['search_case_no'])

# search_case_no = driver.find_element_by_id("rgyear")
# search_case_no.send_keys(config['config1']['rgyear'])



# def form_parsing(html):
#     tree = lxml.html.fromstring(html)
#     # print("tree pppp", tree.cssselect('form input'))
#     data = {}
#     for e in tree.cssselect('form input'):
#         if e.get('name'):
#             data[e.get('name')] = e.get('value')
#     return data


ckj = cookielib.CookieJar()
browser = urllib2.build_opener(urllib2.HTTPCookieProcessor(ckj))
html = browser.open(website_url).read()
# form = form_parsing(html)
print("aaaaaaaaaaaaaaaaaaaaaa")
# pprint.pprint(form)


from io import BytesIO
import lxml.html
from PIL import Image
def get_captcha(html):
   tree = lxml.html.fromstring(html)
   print("tree qqqqqqqqqqqq", type(tree))
   img_data = tree.xpath('/html/body/form/div[8]/div/div[2]/span/div[1]/div/span[3]/img')[0].get('src')
#    img_data = tree.cssselect('div#recaptcha img')[0].get('src')
   print("img_data", img_data)
   img_data = img_data.partition(',')[-1]
   print("hhhhhhhhhhhhhhh", img_data)
   binary_img_data = img_data.decode('base64')
   file_like = BytesIO(binary_img_data)
   img = Image.open(file_like)
   return img

import pytesseract
img = get_captcha(html)
img.save('captcha_original.png')
gray = img.convert('L')
gray.save('captcha_gray.png')
bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
bw.save('captcha_thresholded.png')

captcha_text = pytesseract.image_to_string(bw)

captcha_element = driver.find_element_by_id("captcha")
captcha_element.send_keys(captcha_text)

# driver.find_element_by_name("submit1").click()



