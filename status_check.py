#!/usr/bin/env python3

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import tomlkit
from PIL import Image

# hardcoded config values
school_list_filename = "schools.toml"
summery_filename = ("summery.jpeg")
thumbsize = (700, 700)

# get username and password from environment (same for all schools)
username = os.environ.get("WEB_USER")
password = os.environ.get("WEB_PASS")

# get list of schools to check from toml
toml_string = ""
with open(school_list_filename) as s_file:
    toml_string = s_file.read()
schools = tomlkit.parse(toml_string)['school']

def status_check(url, tar_filename):
    """
    using selenium in firefox mode, visit url (LSAC status check page for school)
    login using username and password exported as environment variable
    save screenshot at tar_filename
    """
    browser = webdriver.Firefox()
    browser.get(url)

    elem = browser.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_txtUsername")
    elem.send_keys(username)

    elem = browser.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_txtPassword")
    elem.send_keys(password)

    elem = browser.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_btnlogon")
    elem.click()

    browser.save_screenshot(tar_filename)
    browser.quit()


# for each school in schools save a screenshot of the status page
for school in schools:
    school_name = schools[school]['name']
    school_url = schools[school]['url']

    school_tar_filename = school_name + '_status.png'
    status_check(school_url, school_tar_filename)

# Create Summery Screenshot, all others combined
summery = None
for index, school in enumerate(schools):
    school_name = schools[school]['name']
    image_filename = school_name + "_status.png"

    im = Image.open(image_filename)
    im.thumbnail(thumbsize)

    if summery == None:
        summery = Image.new("RGB", (im.size[0]*3, im.size[1]*2))

    x = index // 2 * im.size[0]
    y = index % 2 * im.size[1]

    w, h = im.size

    summery.paste(im, (x,y,x+w, y+h))

summery.save(summery_filename)
