import copy
from selenium import webdriver
from selenium.webdriver.common.by import By

__author__ = 'danielevertsson'


OP_PROFILE_DIANA = {
    "givenName": "Diana",
    "mail": "diana@example.org",
    "eduPersonNickname": "Diana",
    "osiOtherEmail": "false",
    "eduPersonTargetedID": None
}


class TestVOPaaS:
    def test_phantom_js(self):
        try:
            driver = webdriver.PhantomJS()
        except:
            driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
        driver.get("https://google.se/")
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

    def test_login_to_OP(self):
        driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs",
                                     service_args=['--ignore-ssl-errors=true'])
        # Go to SP
        driver.get("http://{{ hostname }}:{{ sp_port }}")

        # Pick frontend in DS
        driver.find_element_by_id("to_list").click()
        dropdown = driver.find_element_by_id("thelist")
        for option in dropdown.find_elements_by_tag_name('option'):
            if option.text == "OP - TEST":
                option.click()
                break
        driver.find_element_by_id("proceed").click()

        # Login to OP
        driver.find_element_by_name("login").clear()
        driver.find_element_by_name("login").send_keys("diana")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("krall")
        driver.find_element_by_name("form.commit").click()

        # Give consent
        buttons = driver.find_elements_by_tag_name("button")
        for button in buttons:
            if button.get_attribute("value") == "Yes":
                button.click()
                break

        # Assert return values
        diana_profile = copy.deepcopy(OP_PROFILE_DIANA)
        table_row = driver.find_elements(By.TAG_NAME, "tr")
        for row in table_row:
            cell_header = row.find_elements(By.TAG_NAME, "th")[0].text
            cell_value = row.find_elements(By.TAG_NAME, "td")[0].text
            assert cell_header in diana_profile, "Received unexpected parameter: %s" % cell_header
            if diana_profile[cell_header] is not None:
                expected_value = diana_profile.pop(cell_header, None)
                assert cell_value == expected_value, "The received parameter value did not match the expected " \
                                                     "value: '%s' != '%s'" % (cell_value, expected_value)
        # Assert all parameters was received
        assert not diana_profile, "Did not receive all expected parameters: %s" % list(diana_profile.keys())

