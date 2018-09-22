from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


MAX_WAIT = 10


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # Lain has heard about a cool new online to-do app. She checks
        # its homepage
        self.browser.get(self.live_server_url)

        # Notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.get_item_input_box()
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # types "Buy GE 999 manga" into a text box
        # She hits enter, the page updates, and now the page lists
        # "1: Buy GE 999 manga" as a to-do list item
        self.add_list_item('Buy GE 999 manga')

        # There is still a text box inviting her to add another item.
        # She enters "Watch accompanying anime"
        self.add_list_item('Watch accompanying anime')

        # Page updates again, now shows both items on her list
        self.wait_for_row_in_list_table('2: Watch accompanying anime')
        self.wait_for_row_in_list_table('1: Buy GE 999 manga')

        # Lain wonders whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her --
        # some text explains this

        # She visits the URL - her to-do list is still there.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Lain starts a new to-do list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy GE 999 manga')

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

        self.add_list_item('Buy NAVI')

        # Eri gets his own URL
        eri_list_url = self.browser.current_url
        self.assertRegex(eri_list_url, '/lists/.+')
        self.assertNotEqual(eri_list_url, lain_list_url)

        # Again, no trace of Lain's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy GE 999 manga', page_text)
        self.assertIn('Buy NAVI', page_text)

        # Satisfied, they both wallow in their virtual universes
