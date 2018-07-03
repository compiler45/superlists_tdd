import unittest
from selenium import webdriver


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
        self.fail('Finish the test!')

        # She is invited to enter a to-do item straight away

        # types "Buy GE 999 manga" into a text box

        # She hits enter, the page updates, and now the page lists
        # "1: Buy GE 999 manga" as a to-do list item

        # There is still a text box inviting her to add another item.
        # She enters "Watch accompanying anime"

        # Page updates again, now shows both items on her list

        # Edith wonders whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her --
        # some text explains this

        # She visits the URL - her to-do list is still there.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
