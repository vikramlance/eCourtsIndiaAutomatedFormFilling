"""
Automate filling of the forms on eCourts India website
"""
import sys
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from time import sleep


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
input_config = sys.argv[1]
website_url = config[input_config]['url']

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(website_url)

court_establishment = driver.find_element_by_id("radCourtEst")
court_establishment.click()

select_court_code = Select(driver.find_element_by_id('court_code'))
select_court_code.select_by_value(config[input_config]['court_code'])

select_case_type = Select(driver.find_element_by_id('case_type'))
select_case_type.select_by_value(config[input_config]['case_type'])

search_case_no = driver.find_element_by_id("search_case_no")
search_case_no.send_keys(config[input_config]['search_case_no'])

search_case_no = driver.find_element_by_id("rgyear")
search_case_no.send_keys(config[input_config]['rgyear'])

# driver.save_screenshot('screenshot.png')

# from PIL import Image

# def get_captcha(driver, element, path):
#     # now that we have the preliminary stuff out of the way time to get that image :D
#     location = element.location
#     size = element.size
#     # saves screenshot of entire page
#     driver.save_screenshot(path)

#     # uses PIL library to open image in memory
#     image = Image.open(path)

#     left = location['x'] + 120
#     top = location['y'] + 100
#     right = location['x'] + size['width'] + 120
#     bottom = location['y'] + size['height'] + 100

#     image = image.crop((left, top, right, bottom))  # defines crop points
#     image.save(path, 'png') 

# # change frame
# # driver.switch_to.frame("Main")

# # download image/captcha
# img = driver.find_element_by_xpath('//*[@id="captcha_image"]')
# get_captcha(driver, img, "captcha.png")


# import pytesseract
# import os
# import argparse
# try:
#     import Image, ImageOps, ImageEnhance, imread
# except ImportError:
#     from PIL import Image, ImageOps, ImageEnhance

# def solve_captcha(path):

#     """
#     Convert a captcha image into a text, 
#     using PyTesseract Python-wrapper for Tesseract
#     Arguments:
#         path (str):
#             path to the image to be processed
#     Return:
#         'textualized' image
#     """
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#     image = Image.open(path).convert('RGB')
#     image = ImageOps.autocontrast(image)

#     print("image", image)

#     filename = "{}.png".format(os.getpid())
#     image.save(filename)
#     print("filename", filename)

#     text = pytesseract.image_to_string(Image.open(filename))
#     return text

# captcha_text = solve_captcha('captcha.png')
# print("aaaaaa 3")
# print(captcha_text)

# search_captha = driver.find_element_by_id("captcha")
# search_captha.send_keys(captcha_text)
from selenium.webdriver.support.ui import WebDriverWait

WebDriverWait(driver, 100).until(lambda driver: len(driver.find_element_by_id("captcha").get_attribute("value")) == 6)

# current_url = driver.current_url


driver.find_element_by_name("submit1").click()

sleep(5)
# from selenium.webdriver.support import expected_conditions as EC
# WebDriverWait(driver, 15).until(EC.url_changes(current_url))


driver.find_element_by_xpath('//*[@id="showList1"]/tr/td[4]/a').click()

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

screenshot_name = 'screenshot_' + config[input_config]['case_district'] + '.png'
driver.save_screenshot(screenshot_name)

# driver.Quit()

