from selenium import webdriver
from selenium.webdriver.common.by import By

__author__ = 'danielevertsson'


class TestSaaS:
    def test_phantom_js(self):
        try:
            driver = webdriver.PhantomJS()
        except:
            driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
        driver.get("https://www.google.se/")
        image = driver.find_element_by_id("hplogo")
        assert image.text == "Sverige"

    def test_login_to_idp_1(self):
        driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs",
                                     service_args=['--ignore-ssl-errors=true'])
        driver.get("http://{{ hostname }}:9087")
        driver.find_element_by_id("to_list").click()

        dropdown = driver.find_element_by_id("thelist")
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text == "My IDP NO.1":
                option.click()
                break

        driver.find_element_by_id("proceed").click()
        driver.find_element_by_name("login").clear()
        driver.find_element_by_name("login").send_keys("roland")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("dianakra")
        driver.find_element_by_name("form.submitted").click()
        # driver.get("http://127.0.0.1:9087")

        table_row = driver.find_elements(By.TAG_NAME, "tr")
        found_match = False
        for row in table_row:
            cell = row.find_elements(By.TAG_NAME, "td")
            if cell[0].text == "P. Roland Hedberg":
                found_match = True
        assert found_match
