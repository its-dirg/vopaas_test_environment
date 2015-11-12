# -*- coding: utf-8 -*-
import copy
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

__author__ = 'danielevertsson'


OP_PROFILE_DIANA = {
    "givenName": "Diana",
    "displayName": "Dinka",
    "cn": "Diana Krall",
    "postalAddress": 'UmeÃ¥ Universitet',
    "eduPersonTargetedID": None,
    "email": "diana@example.org",
    "sn": "Krall",
}

IDP_PROFILE_TESTUSER = {
    "givenName": "Test",
    "eduPersonTargetedID": None,
    "displayName": "Test Testsson",
    "sn": "Testsson",
    "email": "mail"
}

def _consent(driver, given=True):
    buttons = driver.find_elements_by_tag_name("button")
    for button in buttons:
        if button.get_attribute("value") == ("Yes" if given else "No"):
            button.click()
            break

def _discovery_server(driver):
    driver.find_element_by_id("to_list").click()
    dropdown = driver.find_element_by_id("thelist")
    for option in dropdown.find_elements_by_tag_name('option'):
        if option.text == "My IDP NO.1":
            option.click()
            break
    driver.find_element_by_id("proceed").click()

def _idp_login_form( driver):
    driver.find_element_by_name("login").clear()
    driver.find_element_by_name("login").send_keys("testuser")
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys("qwerty")
    driver.find_element_by_name("form.submitted").click()

class TestVOPaaS:
    def test_phantom_js(self):
        try:
            driver = webdriver.PhantomJS()
        except:
            driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
        driver.get("https://google.se/")
        image = driver.find_element_by_id("hplogo")
        assert image.text == "Sverige"

    @pytest.mark.parametrize("give_consent", [
        False,
        True,
    ])
    def test_login_to_idp_1(self, give_consent):
        driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs",
                                     service_args=['--ignore-ssl-errors=true'])
        driver.get("{{ host }}:{{ sp_port }}")

        _discovery_server(driver)
        _idp_login_form(driver)
        _consent(driver, give_consent)

        table_row = driver.find_elements(By.TAG_NAME, "tr")
        if give_consent:
            compare_table_with_profile(table_row, IDP_PROFILE_TESTUSER)
        else:
            assert not table_row

    def test_restore_state_at_different_proxy(self):
        driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs",
                                     service_args=['--ignore-ssl-errors=true'])
        driver.get("{{ host }}:{{ sp_2_port }}?IdpQuery=https%3a%2f%2f127.0.0.1%3a9092%2fSaml2IDP"
                   "%2fproxy.xml%2faHR0cDovLzEyNy4wLjAuMTo5MDg4L2lkcDEueG1s")

        _idp_login_form(driver)
        _consent(driver, True)

        table_row = driver.find_elements(By.TAG_NAME, "tr")
        compare_table_with_profile(table_row, IDP_PROFILE_TESTUSER)

    @pytest.mark.parametrize("give_consent", [
        False,
        True,
    ])
    def test_login_to_OP(self, give_consent):
        driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs",
                                     service_args=['--ignore-ssl-errors=true'])
        # Go to SP
        driver.get("{{ host }}:{{ sp_port }}")

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

        _consent(driver, give_consent)

        # Assert return values
        table_row = driver.find_elements(By.TAG_NAME, "tr")

        if give_consent:
            # If given consent, assert all attributes was received
            compare_table_with_profile(table_row, OP_PROFILE_DIANA)
        else:
            # If not given consent, assert no attributes was received
            assert not table_row

def compare_table_with_profile(table, profile):
    profile = copy.deepcopy(profile)
    for row in table:
        cell_header = row.find_elements(By.TAG_NAME, "th")[0].text
        cell_value = row.find_elements(By.TAG_NAME, "td")[0].text
        assert cell_header in profile, "Received unexpected parameter: %s" % cell_header
        expected_value = profile.pop(cell_header, None)
        if expected_value is not None:
            assert cell_value == expected_value, "The received parameter value did not match the expected " \
                                                 "value: '%s' != '%s'" % (cell_value, expected_value)
    # Assert all parameters was received
    assert not profile, "Did not receive all expected parameters: %s" % list(profile.keys())