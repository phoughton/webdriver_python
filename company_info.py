from selenium import webdriver
import requests
import os
import json
from dicttoxml import dicttoxml
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COMPANIES_LIST = "/html/body/section[2]/div[2]/div[2]/div"
COMPANY_DETAILS = "/html/body/section[2]/div[2]/main/div[1]/div/div"
COMPANY_IMAGE = "/html/body/section[2]/div[2]/main/div[1]/div/div/div[1]/div/img"
LOCAL_IMAGES = "company_images"
WEBSITE = "https://www.medicines.org.uk/emc/browse-companies"
ALPHA_LIST = "/html/body/section[2]/div[2]/div[1]/div/ul"


def make_safe(unsafe_string):
    return "".join([c for c in unsafe_string if c.isalpha() or c.isdigit()]).rstrip()


def get_image(url, file_safe_name):
    response = requests.get(url, verify=False,
                            headers={"content-type": 'image/jpg',
                                     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"})

    if not os.path.exists(LOCAL_IMAGES):
        os.makedirs(LOCAL_IMAGES)

    filename = LOCAL_IMAGES + '/' + file_safe_name + '.jpg'

    open(filename, 'wb').write(response.content)
    return filename


def grab_company_details_and_return(driver, element):

    link = element.find_elements_by_tag_name('a')
    company_name = link[0].text
    company_data = {}
    link[0].click()

    company_data['name'] = company_name
    company_data['details'] = driver.find_element_by_xpath(COMPANY_DETAILS).text
    company_data['imgUrl'] = driver.find_element_by_xpath(COMPANY_IMAGE).get_attribute('src')

    company_data['imgFilename'] = get_image(company_data['imgUrl'], make_safe(company_name))

    driver.back()
    return company_data


def get_company_list(driver):
    column_list = driver.find_element_by_xpath(COMPANIES_LIST)
    return column_list.find_elements_by_tag_name('li')


def write_data(the_data):
    json_file = open("company_data.json", "w")
    json_file.write(json.dumps(the_data, indent=4, sort_keys=True))
    json_file.close()

    xml_file = open("company_data.xml", "w")
    xml_file.write(dicttoxml(the_data).decode("UTF-8"))
    xml_file.close()


def main():
    browser = webdriver.Chrome()
    browser.get(WEBSITE)

    all_company_data = []
    privacy_link = browser.find_element_by_link_text("Continue")
    privacy_link.click()

    page_list = browser.find_element_by_xpath(ALPHA_LIST)
    alpha_pages = page_list.find_elements_by_tag_name('a')

    list_of_page_links = []
    for page_link in alpha_pages:
        list_of_page_links.append(page_link.text)

    browser.maximize_window()

    for page_link_text in list_of_page_links:
        page_list = browser.find_element_by_xpath(ALPHA_LIST)

        page_link = page_list.find_element_by_link_text(page_link_text)
        page_link.click()

        number_of_companies = len(get_company_list(browser))

        all_company_data.append(grab_company_details_and_return(browser, get_company_list(browser)[0]))

        if number_of_companies > 2:
            all_company_data.append(grab_company_details_and_return(browser, get_company_list(browser)[2]))

        if number_of_companies > 1:
            all_company_data.append(grab_company_details_and_return(browser, get_company_list(browser)[number_of_companies-1]))

    write_data(all_company_data)
    browser.close()


if __name__ == '__main__':

    main()

