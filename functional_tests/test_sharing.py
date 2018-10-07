from selenium import webdriver

from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage
from functional_tests.my_lists_page import MyListsPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # Lain is a logged-in user
        self.create_pre_authenticated_session('lain@example.com')
        lain_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(lain_browser))

        # Her friend Edith is also hanging out on the lists site
        edith_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(edith_browser))
        self.browser = edith_browser
        self.create_pre_authenticated_session('edith@example.com')

        # Lain goes to the home page and starts a list
        self.browser = lain_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        # She notices a 'Share this list' option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # She shares her list. The page updates to say that it's shared with Edith
        list_page.share_list_with('edith@example.com')

        # Edith now goes to the lists page with her browser
        self.browser = edith_browser
        MyListsPage(self).go_to_my_lists_page()

        # She sees Lain's list in there!
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, Edith can see that it's Lain's list
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'lain@example.com'
        ))

        # She adds an item to the list
        list_page.add_list_item('Hi, Lain!')

        # When Lain refreshes the page, she sees Edith's addition
        self.browser = lain_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi, Lain!', 2)


