import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edit has heard about a cool new online to-do app. She checks
        # its homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy GE 999 manga', [row.text for row in rows])

        # There is still a text box inviting her to add another item.
        # She enters "Watch accompanying anime"
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Watch accompanying anime')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # Page updates again, now shows both items on her list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('2: Watch accompanying anime', [row.text for row in rows])

        # Edith wonders whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her --
        # some text explains this

        # She visits the URL - her to-do list is still there.
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
