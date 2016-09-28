from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

#Begin login logic
def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None
def button_is_loaded(driver):
    return driver.find_element_by_id("form_save") != None

driver = webdriver.Firefox()
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
#end login logic

txtfile = open('vacature_links.txt', 'ab')

#Obtain search results. write all urls for search into txt file. adjust range based on total # of pages. this can be done dynamically later
for i in range(0, 17337):
    url = "http://www.nationalevacaturebank.nl/werkgever/cv-zoeken/overzicht/wijzigingsdatum/uitgebreid/page/" + str(i) + "/query//distance/30/output/html/anonymous/anonymous-2-niet-anoniem/load_mode/results_page/items_per_page/50/ignore_ids"
    print "===Page===" + url
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_is_loaded)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,"html5lib")
    cv_links = soup.find_all('li', {'class':'result-item'})
    for cv_link in cv_links:
        cv_link_text = cv_link.find('a')
        cv_link_text = str(cv_link_text.attrs['href'])
        print cv_link_text
        cv_link_text = BeautifulSoup(str(cv_link_text).strip()).get_text().encode("utf-8").replace("\n", " ")
        txtfile.write(cv_link_text + "\n")
