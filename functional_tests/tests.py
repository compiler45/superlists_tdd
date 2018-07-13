import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Lain has heard about a cool new online to-do app. She checks
        # its homepage
        self.browser.get(self.live_server_url)

        # Notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # types "Buy GE 999 manga" into a text box
        input_box.send_keys('Buy GE 999 manga')

        # She hits enter, the page updates, and now the page lists
        # "1: Buy GE 999 manga" as a to-do list item
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy GE 999 manga')

        # There is still a text box inviting her to add another item.
        # She enters "Watch accompanying anime"
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Watch accompanying anime')
        input_box.send_keys(Keys.ENTER)

        # Page updates again, now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy GE 999 manga')
        self.wait_for_row_in_list_table('2: Watch accompanying anime')

        # Lain wonders whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her --
        # some text explains this

        # She visits the URL - her to-do list is still there.
        self.fail('Finish the test!')

    def test_can_start_a_list_for_one_user(self):
        # Lain has heard about a cool new online to-do app, she goes to
        # [...]
        # page updates, shows both items in her list
        self.wait_for_row_in_list_table('2: Watch accompanying anime')
        self.wait_for_row_in_list_table('1: Buy GE 999 manga')

        # Satisfied, she immerses herself in the Wired late at night

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Lain starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy GE 999 manga')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy GE 999 manga')

        # notices that her list has a unique URL
        lain_list_url = self.browser.current_url
        self.assertRegex(lain_list_url, '/lists/.+')

        # Now a new user, Eri, comes along to the site

        ## We use a new browser session to make sure that no information
        ## of Lain's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Eri visits the home page. There is no sign of Lain's 
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy GE 999 manga', page_text)
        self.assertNotIn('Watch accompanying anime', page_text)

        # Eri starts a new list by entering a new item He
        # is less interesting than Lain

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy NAVI')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('Buy NAVI')

        # Eri gets his own URL
        eri_list_url = self.browser.current_url
        self.assertRegex(eri_list_url, '/lists/.+')
        self.assertNotEqual(eri_list_url, lain_list_url)

        # Again, no trace of Lain's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy GE 999 manga', page_text)
        self.assertIn('Buy NAVI', page_text)

        # Satisfied, they both wallow in their virtual universes
