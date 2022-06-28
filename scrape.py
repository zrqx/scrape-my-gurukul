import re
import time
import json
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

parser = argparse.ArgumentParser()
browser = webdriver.Firefox(executable_path="./drivers/geckodriver")
url = "http://my-gurukul.com/login.aspx?CF=E365&SID=1040"

meta = {}

parser.add_argument('-u','--usn',help='USN of the Student')
parser.add_argument('-p','--password',help='Password for the USN')
args = parser.parse_args()

def login(usn,password):
    usn_input = browser.find_element_by_css_selector('#txtUserName')
    password_input = browser.find_element_by_css_selector('#txtPassword')
    submit_btn = browser.find_element_by_css_selector('#Validate')
    usn_input.clear()
    usn_input.send_keys(usn)
    password_input.send_keys(password)
    submit_btn.click()

def enter_submenu(identifier):
    entrypoint = browser.find_element_by_css_selector(identifier)
    entrypoint.click()
    browser.switch_to_default_content()
    iframe = browser.find_element_by_xpath('//*[@id="mygurukuliframe"]')
    browser.switch_to_frame(iframe)

def exit_submenu():
    browser.switch_to_default_content()
    back_btn = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#tdBackMenuIcon")))
    back_btn.click()
    iframe = browser.find_element_by_xpath('//*[@id="mygurukuliframe_submenu"]')
    browser.switch_to_frame(iframe)

def get_attribute_value(selector):
    return WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,selector))).get_attribute('value')

# Authenticate
browser.get(url)
login(args.usn,args.password)

try:
    error = WebDriverWait(browser,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#txtfailedmsg")))
    if (error):
        login(args.usn,args.password)
except:
    pass
   
# Individual Pages
try:
    iframe = browser.find_element_by_xpath('//*[@id="mygurukuliframe_submenu"]')
    browser.switch_to_frame(iframe)
except:
    print('Use EC.XPATH')

## Profile
def profile_submenu(meta):
    enter_submenu('#imgid_0')
    course_info = {}
    personal = {
        "name" : get_attribute_value("#txtFirstname"),
        "dob" : get_attribute_value("#txtDOB"),
        "email" : get_attribute_value("#txtEmailId"),
        "aadhar_number" : get_attribute_value("#txtAadharNo")
    }
    course_info["course_details"] = get_attribute_value("#txtCourse").replace(' ','')
    meta["personal"] = personal
    meta["course_info"] = course_info
    exit_submenu()
    return meta

## Dashboard
def dashboard_submenu(meta):
    enter_submenu('#imgid_1')
    meta["personal"]["father_name"] = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#FatherName"))).text
    exit_submenu()
    return meta

##  View Performance Details
def performance_submenu(meta):
    enter_submenu('#imgid_19')
    table = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"tr:nth-child(2)")))
    table = browser.find_elements(By.TAG_NAME,'tr')
    count = 0
    data_array = []
    for each in table:
        if (count != 0):
            test_count = tests
            pattern = '[^\s]+\s+[^[0-9]+'
            string = str(each.text)
            result = re.match(pattern,string)
            data_object = {}
            subject_name = result[0][:-1].replace(' ','-')
            extras = list(string.replace(result[0][:-1],'')[1:].split(' '))
            xcount = 1

            data_object = {
                "subject_name" : subject_name,
                "subject_code" : extras[0],
                "class_held" : extras[1],
                "class_attended" : extras[2],
                "tests" : test_count
            }

            while (test_count != 0):
                data_object[f"test{xcount}"] = extras[5+xcount]
                test_count -= 1
                xcount += 1
            data_array.append(data_object)
        else:
            headers = each.text
            headerlist = list(headers.split(' '))
            tests = len(headerlist[11:])
        count += 1
    meta["performance"] = data_array
    exit_submenu()
    return meta

# Manage Student Registrations
def manage_registrations_submenu(meta):
    enter_submenu('#imgid_29')
    ## Enter another Iframe
    iframe = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#frameRegister1")))
    browser.switch_to_frame(iframe)
    ## Selecting
    table = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.TAG_NAME,"tr")))
    table = browser.find_elements(By.TAG_NAME,'tr')
    data_array = []
    count = 0
    for each in table:
        if (count != 0):
            data_object = {}
            pattern = "\s[A-Z][A-Z,a-z,\s]+"
            string = str(each.text)
            result = re.search(pattern,string)
            extras = list(string.replace(result[0],' ').split(' '))
            data_object = {
                "subject_name" : result[0][1:-1],
                "subject_code" : extras[1],
                "credits" : extras[3],
                "type" : extras[4]
            }
            data_array.append(data_object)
        count += 1
    meta["registered_courses"] = data_array
    exit_submenu()
    return meta

# Main
meta = performance_submenu(meta)
meta = profile_submenu(meta)
meta = dashboard_submenu(meta)
meta = manage_registrations_submenu(meta)
print(json.dumps(meta,indent=4))

# Close
browser.close()
