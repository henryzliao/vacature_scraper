from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import csv
import shutil

def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None
def button_is_loaded(driver):
    return driver.find_element_by_id("form_save") != None

#Set up file downloader
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.openFile", "application/pdf,application/msword,application/xml,application/octet-stream");
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/msword,application/xml,application/octet-stream");
fp.set_preference("browser.helperApps.alwaysAsk.force", False);

#Set up login as before
driver = webdriver.Firefox(firefox_profile=fp)
driver.set_window_size(1080,800)
driver.get("http://www.nationalevacaturebank.nl/werkgever")

wait = ui.WebDriverWait(driver, 10)
wait.until(button_is_loaded)

#html = driver.page_source
#soup = BeautifulSoup(html, "html5lib")
#print soup

driver.find_element_by_class_name('button').click()
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

#html = driver.page_source
#soup = BeautifulSoup(html, "html5lib")
#print soup

wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)
email_field = driver.find_element_by_id("emailadresjqiho")
email_field.send_keys("rtdcarrierevacatures@gmail.com")
password_field = driver.find_element_by_id("password")
password_field.send_keys("WPA2957134")
password_field.send_keys(Keys.RETURN)

#html = driver.page_source
#soup = BeautifulSoup(html,"html5lib")
#print soup

#Obtain cv data, parse and write to csv. download cv file (usually word doc) and store name with profile data
csvfile = open('vacature_profiles.csv', 'ab')
writer = csv.writer(csvfile, delimiter = '|', quotechar = '"')
with open('vacature_links.txt') as f:
    for url in f:
        print "===Page===" + url
        wait = ui.WebDriverWait(driver, 10)
        wait.until(page_is_loaded)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,"html5lib")
        profile_data = soup.find_all('div', {'class':'tab-contents'})
        #print profile_data
        if not profile_data:
            continue
        candidate_number = ""
        revision_date = ""
        most_recent_function = ""
        most_recent_employer = ""
        career_level = ""
        education_level = ""
        drivers_license = ""
        desired_function = ""
        desired_function_group = ""
        desired_industry = ""
        availability = ""
        hours = ""
        employment = ""
        max_travel = ""
        salary = ""
        photo_url = ""
        basic_info = ""
        name = ""
        address = ""
        phone = ""
        email = ""
        cv_file_name = ""
        skip_function = 0
        skip_employer = 0
        skip_drivers_license = 0
        for profile in profile_data:
            tab1 = profile.find_all('div', {'id':'tab-1'})
            for tab1_data in tab1:
                tab1_list_headings = tab1_data.findAllNext('dt')
                print tab1_list_headings
                print tab1_list_headings[2].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                #print tab1_list_headings[3].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                if tab1_list_headings[2].get_text().strip().encode('ascii', 'ignore').decode('ascii')[0] == "C":
                     #print "skipping function"
                     skip_function = 1
                     if tab1_list_headings[3].get_text().strip().encode('ascii', 'ignore').decode('ascii')[0] == "O":
                         skip_employer = 1
                if tab1_list_headings[3].get_text().strip().encode('ascii', 'ignore').decode('ascii')[0] == "C":
                     skip_employer = 1
                if tab1_list_headings[4].get_text().strip().encode('ascii', 'ignore').decode('ascii')[0] == "G":
                     skip_drivers_license = 1
                tab1_list = tab1_data.findAllNext('dd')
                candidate_number = tab1_list[0].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                revision_date = tab1_list[1].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                if skip_drivers_license == 1:
                    career_level = tab1_list[2].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    education_level = tab1_list[3].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_function = tab1_list[4].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_function_group = tab1_list[5].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_industry = tab1_list[6].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    availability = tab1_list[7].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    hours = tab1_list[8].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    employment = tab1_list[9].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    max_travel = tab1_list[10].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    salary = tab1_list[11].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                elif skip_function == 1 and skip_employer == 1:
                    most_recent_function = ""
                    most_recent_employer = ""
                    career_level = tab1_list[2].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    education_level = tab1_list[3].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    drivers_license = tab1_list[4].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_function = tab1_list[5].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_function_group = tab1_list[6].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_industry = tab1_list[7].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    availability = tab1_list[8].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    hours = tab1_list[9].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    employment = tab1_list[10].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    max_travel = tab1_list[11].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    salary = tab1_list[12].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                elif skip_employer == 1:
                    most_recent_function = tab1_list[2].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    most_recent_employer = ""
                    career_level = tab1_list[3].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    education_level = tab1_list[4].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    drivers_license = tab1_list[5].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_function = tab1_list[6].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_function_group = tab1_list[7].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_industry = tab1_list[8].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    availability = tab1_list[9].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    hours = tab1_list[10].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    employment = tab1_list[11].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    max_travel = tab1_list[12].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    salary = tab1_list[13].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                else:
                    most_recent_function = tab1_list[2].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    most_recent_employer = tab1_list[3].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    career_level = tab1_list[4].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    education_level = tab1_list[5].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    drivers_license = tab1_list[6].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_function = tab1_list[7].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_function_group = tab1_list[8].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    desired_industry = tab1_list[9].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    availability = tab1_list[10].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    hours = tab1_list[11].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    employment = tab1_list[12].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    max_travel = tab1_list[13].get_text().strip().encode('ascii', 'ignore').decode('ascii')
                    salary = tab1_list[14].get_text().strip().encode('ascii', 'ignore').decode('ascii')
            print "candidate number: " + candidate_number
            print "\n revision date: " + revision_date
            print "\n recent function: " + most_recent_function
            print "\n recent employer: " + most_recent_employer
            print "\n career level: " + career_level
            print "\n education level: " + education_level
            print "\n driver's license: " + drivers_license
            print "\n desired function: " + desired_function
            print "\n desired function group: " + desired_function_group
            print "\n desired industry: " + desired_industry
            print "\n availability: " + availability
            print "\n hours: " + hours
            print "\n employment: " + employment
            print "\n max_travel: " + max_travel
            print "\n salary: " +  salary
            tab2 = profile.find_all('div', {'id':'tab-2'})
            for tab2_data in tab2:
                photo_url_html = tab2_data.find("img")
                photo_url = photo_url_html["src"]
                basic_info = str(tab2_data.findNext('dd'))
                #print basic_info
                basic_info_list = basic_info.split("<br/>")
                #print basic_info_list
                name = basic_info_list[0].split("<dd>")[1].strip()
                address = basic_info_list[1].strip()
                phone = basic_info_list[2].strip()
                email = tab2_data.find("a").get_text().strip().encode('ascii', 'ignore').decode('ascii')
            print "\n photo url: " + photo_url
            print "\n name: " +  name
            print "\n address: " + address
            print "\n phone: " + phone
            print "\n email: " + email
        driver.find_element_by_id("cv-download").click()
        #before = os.listdir(os.getcwd())
        #after = os.listdir(os.getcwd())
        #change = set(after) - set(before)
        #if len(change) == 1:
        #    cv_file_name = change.pop()
        #else:
        #    print "more than one file or no file downloaded"
        cv_file_name = max([f for f in os.listdir(os.getcwd())], key=os.path.getctime)
        print "\n cv file name: " + cv_file_name
        writer.writerow([url,candidate_number,revision_date,most_recent_function,most_recent_employer,career_level,education_level,drivers_license,desired_function,desired_function_group,desired_industry,availability,hours,employment,max_travel,salary,photo_url,name,address,phone,email,cv_file_name])
