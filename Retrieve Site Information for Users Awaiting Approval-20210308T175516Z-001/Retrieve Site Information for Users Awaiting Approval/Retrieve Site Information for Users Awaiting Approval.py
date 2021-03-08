#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import time
import keyring
import openpyxl
from openpyxl import load_workbook
import pandas as pd
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
)
import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager


# ## Required Libraries
# #### os (Installed with python)
# #### time (Installed with python)
# #### keyring (conda install -c anaconda keyring)
# #### openpyxl (conda install -c anaconda openpyxl)
# #### pandas (conda install pandas)
# #### selenium (conda install -c anaconda selenium)
# #### chromedriver_binary (conda install -c conda-forge python-chromedriver-binary=87)
#    ###### NOTE: Replace "=87" with whatever version of Chrome you have running. Don't include numbers after first decimal.
# #### webdriver_manager (pip install webdriver_manager)

# # Get Site Information for Users Awaiting Approval

# In[1]:


# function to take care of downloading file
def enable_download_headless(browser, download_dir):
    browser.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_dir, },

    }
    browser.execute("send_command", params)


# instantiate a chrome options object so you can set the size and headless preference
# some of these chrome options might be uncessary but I just used a boilerplate
# change the <path_to_download_default_directory> to whatever your default download folder is located
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--verbose")
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "<path_to_download_default_directory>",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
    },
)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
driver = webdriver.Chrome()

# Portal Page
driver.get("https://www.dcphrapps.dphe.state.co.us/Account/Login")

###################################################################
# Insert Your Log In Credentials
###################################################################
#Log in
username = driver.find_element_by_name("Email")
username.clear()
username.send_keys("USERNAME/EMAIL")

password = driver.find_element_by_name("Password")
password.clear()
password.send_keys("YOUR PASSWORD")
##################################################################

driver.find_element_by_css_selector('[value="Log in"]').click()
time.sleep(1)

# Click “Portal”
driver.find_element_by_id("DashButton").click()

# Make window full screen
driver.maximize_window()
time.sleep(3)

# Select "Show All"
show_all = Select(driver.find_element_by_name("ActiveUserList_length"))
show_all.select_by_visible_text("25")
time.sleep(3)


driver.find_element_by_xpath('/html/body/div/div/div/div/div/main/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr[1]/td[1]/div/a[1]/span').click()

# Get users registered for each site
items = range(1,25)
for i in items:
    try:
        time.sleep(2)
        #driver.execute_script("window.scrollTo(0, window.scrollY + 600)")
        time.sleep(2)
        FName = driver.find_element_by_xpath('//*[@id="FirstName"]')
        LName = driver.find_element_by_xpath('//*[@id="LastName"]')
        email = driver.find_element_by_xpath('//*[@id="UserName"]')
        Site = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/form[2]/div/div[2]/div[5]/ul/li[1]/div/div[3]/ul/li/div[2]/div/div[2]/ul/li/span')
        print(FName.get_attribute("value"),",",LName.get_attribute("value"),",",email.get_attribute("value"),",",Site.text)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div/ul/li/a').click()
        time.sleep(3)
        show_all = Select(driver.find_element_by_name("ActiveUserList_length"))
        show_all.select_by_visible_text("25")
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/main/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr[%d]/td[1]/div/a[1]/span' % i).click()
        continue
    except (ElementNotVisibleException, NoSuchElementException):
        time.sleep(2)
        #driver.execute_script("window.scrollTo(0, window.scrollY + 600)")
        time.sleep(2)
        FName = driver.find_element_by_xpath('//*[@id="FirstName"]')
        LName = driver.find_element_by_xpath('//*[@id="LastName"]')
        email = driver.find_element_by_xpath('//*[@id="UserName"]')
        print(FName.get_attribute("value"),",",LName.get_attribute("value"),",",email.get_attribute("value"),",", "No Site Info")
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div/div/ul/li/a').click()
        time.sleep(3)
        show_all = Select(driver.find_element_by_name("ActiveUserList_length"))
        show_all.select_by_visible_text("25")
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/main/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr[%d]/td[1]/div/a[1]/span' % i).click()
        pass

